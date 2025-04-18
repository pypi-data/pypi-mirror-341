import asyncio
import logging
import time
from asyncio import Future
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Iterable,
    Literal,
    ParamSpec,
    TypeVar,
)

import httpx
from pydantic import Field, HttpUrl, validate_call

import ton_connect.model.app.response as app_responses
import ton_connect.model.wallet.event as wallet_events
from ton_connect.bridge import Bridge, BridgeMessage, Connection, Session
from ton_connect.model.app.request import (
    AppRequestType,
    ConnectRequest,
    TonAddressRequestItem,
    TonProofRequestItem,
)
from ton_connect.model.app.response import AppResponses
from ton_connect.model.app.wallet import WalletApp
from ton_connect.model.model import BaseModel
from ton_connect.model.wallet.device import Device
from ton_connect.model.wallet.event import (
    TonAddressItem,
    WalletEventName,
    WalletEventType,
)
from ton_connect.model.wallet.wallet import Account
from ton_connect.storage import BridgeData, BridgeKey, BridgeStorage

T = TypeVar("T")
C = TypeVar("C")
TC = TypeVar("TC", bound="TonConnect")
P = ParamSpec("P")

Decorator = Callable[
    Concatenate[TC, P],
    Callable[Concatenate[TC, P], Callable[Concatenate[TC, P], Awaitable[C]]],
]
Decorated = Callable[Concatenate[TC, P], Awaitable[C]]

D = Callable[[Concatenate[TC, P], Awaitable[None]], None]

LOG = logging.getLogger(__name__)

EventListener = Callable[["ConnectorEvent"], Awaitable[None]]

P = ParamSpec("P")
R = TypeVar("R")


ListenerEvent = WalletEventName | Literal["heartbeat", "stopped", "app"]


class ConnectorEvent(BaseModel):
    wallet_name: str = Field(..., description="Wallet name")
    event: WalletEventType | AppResponses = Field(..., description="Event")
    device: Device | None = Field(..., description="User device info")
    account: Account | None = Field(..., description="User account info")
    entity_id: str = Field(..., description="Entity ID")


class Task:
    def __init__(self, func: Callable[P, R], *args: P.args) -> None:
        self.func = func
        self.args = args

    async def __call__(self) -> R:
        try:
            result = self.func(*self.args)
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as e:
            LOG.error(f"Error processing task {self.func}: {e}")


class ConnectionExistsError(Exception):
    pass


class RPCError(Exception):
    pass


class ConnectionNotFoundError(Exception):
    pass


class ConnectionSourceNotFoundError(Exception):
    pass


class ConnectionSessionNotFoundError(Exception):
    pass


class TonConnect:
    APPS = {}
    APPS_CACHE_TTL = 10 * 60
    APPS_URL = "https://raw.githubusercontent.com/ton-blockchain/wallets-list/main/wallets-v2.json"

    def __init__(
        self,
        manifest_url: HttpUrl,
        storage: BridgeStorage,
    ) -> None:
        """Init TON Connector.

        :param manifest_url: URL to manifest file of your app.
        :param storage: Storage for connection data.
        """

        self.manifest_url: HttpUrl = manifest_url
        self.storage: BridgeStorage = storage

        self.queue: asyncio.Queue[BridgeMessage] = asyncio.Queue()
        self.bridges: dict[str, Bridge] = {}
        self.lock = asyncio.Lock()
        self.send_lock = asyncio.Lock()

        self.listeners: dict[ListenerEvent, EventListener] = {}

        self.listener_started = asyncio.Event()
        self.listener: asyncio.Task | None = None

        self.rpc_response_waiters: dict[int, asyncio.Future[Any]] = {}

    def set_bridge(self, app_name: str, bridge: Bridge) -> None:
        self.bridges[app_name] = bridge

    def get_bridge(self, app_name: str) -> Bridge | None:
        return self.bridges.get(app_name)

    @staticmethod
    def ensure_listener(func: Decorator) -> Decorated:
        async def wrapper(self: TC, *args: P.args, **kwargs: P.kwargs) -> C:
            async with self.lock:
                if self.listener is None:
                    self.listener = asyncio.create_task(self.start_listener())
                    await self.listener_started.wait()
            return await func(self, *args, **kwargs)

        return wrapper

    @classmethod
    async def get_wallets(
        cls,
        app_names: list[str] | None = None,
        names: list[str] | None = None,
        ton_dns: list[str] | None = None,
        only_supported: bool = True,
        platforms: list[str] | None = None,
    ) -> list[WalletApp]:
        """Get list of supported wallet apps.

        :param app_names: List of wallet app names to filter wallets.
        :param names: List of wallet names to filter wallets.
        :param ton_dns: List of TON DNS names to filter wallets.
        :param only_supported: Get only supported wallets (python compatible).
        :param platforms: List of platforms to filter wallets.
        :return: List of wallet apps.
        """

        if cls.APPS.get("last_timestamp", 0) + cls.APPS_CACHE_TTL < time.time():
            async with httpx.AsyncClient() as client:
                response = await client.get(cls.APPS_URL)
                response_apps = [WalletApp.model_validate(wallet) for wallet in response.json()]
                cls.APPS["last_timestamp"] = time.time()
                cls.APPS["apps"] = response_apps

        apps: Iterable[WalletApp] = (app for app in cls.APPS["apps"])

        apps = filter(lambda app: app.name in names, apps) if names else apps
        apps = (
            filter(lambda app: set(app.platforms).intersection(platforms), apps)
            if platforms
            else apps
        )
        apps = filter(lambda app: app.is_supported, apps) if only_supported else apps
        apps = filter(lambda app: app.app_name in app_names, apps) if app_names else apps
        apps = filter(lambda app: app.dns in ton_dns, apps) if ton_dns else apps

        return list(apps)

    @ensure_listener
    @validate_call
    async def connect(self, wallet: WalletApp, ton_proof: TonProofRequestItem | None = None) -> str:
        """Connect to the wallet.

        :param wallet: Wallet to connect.
        :param ton_proof: TON proof request item.
        :return: Connection URL.
        """

        async with self.lock:
            connection = await self.storage.get_connection(wallet.app_name)
            if connection is not None and connection.connect_event:
                raise ConnectionExistsError(
                    "Connection already exists. Use restore_connection method."
                )

            bridge = self.get_bridge(wallet.app_name)
            if bridge is not None and bridge.is_alive:
                await bridge.disconnect(send_event=True)
                await asyncio.sleep(0.2)

            await self.storage.delete(wallet.app_name)
            await self.storage.insert(wallet.app_name, BridgeData())

            ready = asyncio.Event()

            bridge = Bridge(
                wallet.app_name,
                self.queue,
                connector_ready=ready,
                bridge_url=wallet.bridge_url,
                universal_url=wallet.universal_url,
            )

            await bridge.register_session()
            await bridge.connected.wait()

            self.set_bridge(wallet.app_name, bridge)

            if connection is None:
                session = Session(
                    private_key=bridge.crypto.private_key.encode().hex(),
                    bridge_url=bridge.bridge_url,
                )

                connection = Connection(
                    session=session,
                    source=wallet.app_name,
                )

            await self.storage.set_connection(wallet.app_name, connection)

            request_items: list[TonAddressRequestItem | TonProofRequestItem] = [
                TonAddressRequestItem()
            ]
            if ton_proof:
                request_items.append(ton_proof)

            request = ConnectRequest(manifest_url=str(self.manifest_url), items=request_items)
            ready.set()

            return bridge.generate_connect_url(request, bridge.crypto.public_key)

    @ensure_listener
    @validate_call
    async def restore_connection(self, wallet: WalletApp) -> Bridge:
        """Restore connection to the wallet."""

        async with self.lock:
            connection = await self.storage.get_connection(wallet.app_name)
            if not connection:
                LOG.info("Connection not found for %s. Use .connect", wallet.app_name)
                raise ConnectionNotFoundError()

            if not connection.source:
                LOG.info("Connection source not found for %s", wallet.app_name)
                raise ConnectionSourceNotFoundError()

            if not connection.session:
                LOG.info("Connection session not found for %s", wallet.app_name)
                raise ConnectionSessionNotFoundError()

            ready = asyncio.Event()

            bridge = Bridge(
                wallet.app_name,
                self.queue,
                connector_ready=ready,
                bridge_url=connection.session.bridge_url,
                universal_url=wallet.universal_url,
                private_key=connection.session.private_key.hex(),
                last_rpc_event_id=connection.last_rpc_event_id,
            )

            await bridge.register_session()

            self.set_bridge(wallet.app_name, bridge)

            ready.set()

            LOG.debug(
                "Waiting for bridge connection %s %s",
                self.storage.entity_id,
                wallet.app_name,
            )

            await bridge.connected.wait()

            LOG.debug("Bridge connected %s %s", self.storage.entity_id, wallet.app_name)

            return bridge

    async def handle_message(self, connection: Connection, message: BridgeMessage) -> None:
        """Handle queue message."""

        int_tasks: list[Task] = []

        if message.event != "heartbeat":
            LOG.info("Handling message: %s", message)

        match message.event:
            case "heartbeat":
                LOG.debug("Heartbeat received")
                await self.storage.set(message.app_name, BridgeKey.HEARTBEAT, int(time.time()))
                return

            case "stopped":
                LOG.info("Bridge %s stopped", message.app_name)
                self.bridges.pop(message.app_name)
                await self.storage.remove(message.app_name, BridgeKey.CONNECTION)
                return

            case wallet_events.ConnectSuccessEvent():
                connection.last_wallet_event_id = message.event.id
                if message.event.payload.find_item_by_type(TonAddressItem) is not None:
                    connection.session.wallet_key = message.source
                    connection.connect_event = message.event
                await self.storage.set_connection(message.app_name, connection)

            case wallet_events.DisconnectEvent() | wallet_events.ConnectErrorEvent():
                LOG.info("Disconnecting from %s for %s", message.app_name, self.storage.entity_id)

                bridge = self.get_bridge(message.app_name)
                int_tasks.append(Task(bridge.disconnect))
                int_tasks.append(Task(self.storage.delete, message.app_name))

            case (
                app_responses.SendTransactionResponseError()
                | app_responses.SendTransactionSuccess()
                | app_responses.SignDataResponseError()
                | app_responses.SignDataSuccess()
            ):
                if message.event.id in self.rpc_response_waiters:
                    # Targeted responses are not handled by listeners
                    self.rpc_response_waiters.pop(message.event.id).set_result(message)
                    return
                elif self.listeners.get("app") is None:
                    LOG.error(
                        "Unexpected App message: %s. "
                        "Register `app` listener to handling wallet app events",
                        message,
                    )

                connection.last_rpc_event_id = message.event.id

            case _:
                LOG.error(f"Unhandled event: {message.event}")

        event_name = "app" if isinstance(message.event, AppResponses) else message.event.name

        if event_name in self.listeners:
            connection = await self.storage.get_connection(message.app_name)

            account = None
            device = None

            if connection.connect_event:
                account = connection.connect_event.payload.find_item_by_type(TonAddressItem)
                device = connection.connect_event.payload.device

            connector_event = ConnectorEvent(
                wallet_name=message.app_name,
                event=message.event,
                device=device,
                account=account,
                entity_id=self.storage.entity_id,
            )
            asyncio.create_task(self.listeners[event_name](connector_event))
        elif isinstance(message.event, WalletEventType):
            LOG.error(f"Unhandled event: {message.event}")

        for task in int_tasks:
            asyncio.create_task(task())

    async def start_listener(self) -> None:
        """Listen for wallet events."""

        LOG.debug("Starting TonConnector event listener...")

        self.listener_started.set()

        try:
            while True:
                try:
                    message: BridgeMessage = await self.queue.get()
                    LOG.debug(f"Event received: {message}")

                    async with self.lock:
                        bridge = self.get_bridge(message.app_name)
                        connection = await self.storage.get_connection(message.app_name)
                        if connection is None:
                            LOG.error(f"Connection not found for {message.app_name}")
                            await self.bridges.get(message.app_name).disconnect(send_event=False)
                            LOG.info(f"Bridge {message.app_name} stopped")
                            continue

                        # 5 Seconds timeout for handling message so we can continue to listen
                        await asyncio.wait_for(
                            self.handle_message(connection, message),
                            timeout=5,
                        )

                        # Update connection with last_rpc_event_id
                        connection.last_rpc_event_id = bridge.last_rpc_event_id
                        await self.storage.set_connection(message.app_name, connection)

                except Exception as e:
                    LOG.exception(f"Error processing event: {message} {type(e)}({e})")
                else:
                    self.queue.task_done()

        except asyncio.CancelledError:
            LOG.debug("TonConnector event listener stopped. Stopping bridge listeners...")
            for bridge in self.bridges.values():
                await bridge.disconnect(send_event=False)
        finally:
            self.listener = None
            self.listener_started.clear()

    async def stop_listener(self) -> None:
        """Stop listener."""

        if self.listener is not None:
            self.listener.cancel()
            await self.listener

    @ensure_listener
    @validate_call
    async def listen(
        self,
        event: ListenerEvent,
        handler: EventListener,
    ) -> None:
        """Add listener to the event.

        :param event: Event name.
        :param handler: Event handler.
        """

        if event in self.listeners:
            raise ValueError(f"Event {event} is already registered")

        self.listeners[event] = handler

    @validate_call
    async def send(
        self,
        app_name: str,
        request: AppRequestType,
        wait_response: bool = True,
        timeout: int = 5,
    ) -> asyncio.Future[app_responses.AppResponses] | None:
        """Send request to the wallet.

        :param app_name: Wallet app name.
        :param request: Request to send.
        :param wait_response: Wait for response. Return task if True.
        :param timeout: Timeout for sending request.
        """

        async with self.send_lock:
            bridge = self.get_bridge(app_name)
            if bridge is None:
                raise Exception("Bridge not found")

            connection = await self.storage.get_connection(app_name)
            if connection is None:
                raise RuntimeError("Connection not found")

            request.id = connection.next_rpc_request_id
            connection.next_rpc_request_id += 1

            await self.storage.set_connection(app_name, connection)

            ttl = 5 * 60

            response = await bridge.send_request(
                request,
                wallet_app_key=connection.session.wallet_key,
                ttl=ttl,
                timeout=timeout,
            )

        LOG.info("Got response for request %s: %s", request.id, response)

        if response["statusCode"] == 200 and wait_response:
            ready: asyncio.Future[app_responses.AppResponses] = Future()
            self.rpc_response_waiters[request.id] = ready

            return ready

        elif response["statusCode"] != 200:
            raise RPCError(response)

        return None
