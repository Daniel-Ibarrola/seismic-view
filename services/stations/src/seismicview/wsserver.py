import asyncio
import janus
import json
import logging
import signal
from socketlib.utils.logger import get_module_logger
import threading
import time
from typing import Callable, Optional
import websockets

from seismicview import CONFIG


class WSServer:
    """A websocket server that sends stations data continuously to multiple clients.

        The station data is sent in json format and has the following schema:

        data = {
            "station": str,
            "channel": str,
            "min": float,
            "max": float,
            "avg": float,
            "trace": list[float]
        }
    """
    def __init__(
            self,
            address: tuple[str, int],
            to_send: Optional[janus.AsyncQueue[bytes]],
            logger: Optional[logging.Logger] = None
    ):
        self.host = address[0]
        self.port = address[1]

        self._to_send = to_send

        if logger is not None:
            self._logger = logger
        else:
            self._logger = get_module_logger(__name__, CONFIG.NAME, use_file_handler=False)

        self.connections = {}  # type: dict[websockets.WebSocketServerProtocol, str]

    @property
    def to_send(self) -> janus.AsyncQueue:
        return self._to_send

    def add_stop_listener(self, listener: Optional[Callable] = None, *args):
        loop = asyncio.get_event_loop()
        for sig_name in {'SIGINT', 'SIGTERM'}:
            if listener is None:
                loop.add_signal_handler(getattr(signal, sig_name),
                                        lambda: asyncio.ensure_future(self.stop()))
            else:
                loop.add_signal_handler(getattr(signal, sig_name),
                                        lambda: asyncio.ensure_future(listener(*args)))

    async def stop(self) -> None:
        self._logger.info("Stopping WebSocket Server...")
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)
        asyncio.get_event_loop().stop()

    @staticmethod
    async def send_station_data(
            data: bytes,
            connections: dict[websockets.WebSocketServerProtocol, str],
    ) -> None:
        """ Sends the most recent message to all clients, if the requested
            station is the same as the one in the message.
        """
        if connections:
            data_str = data.decode()
            data_json = json.loads(data_str)
            current_station = data_json["station"]
            for ws, station in connections.items():
                if station == current_station:
                    try:
                        await ws.send(data_str)
                    except websockets.ConnectionClosedOK:
                        continue

    async def handle_new_connection(
            self,
            ws: websockets.WebSocketClientProtocol
    ) -> None:
        try:
            station = await ws.recv()
        except websockets.ConnectionClosed:
            del self.connections[ws]
            return

        self._logger.info(f"{ws.id} connected. Requested station {station}")

        self.connections[ws] = station

        try:
            await ws.wait_closed()
        finally:
            self._logger.info(f"Disconnected {ws.id}")
            del self.connections[ws]

    async def send(self) -> None:
        while True:
            msg = await self._to_send.get()
            await self.send_station_data(msg, self.connections)

    async def start(self) -> None:
        self._logger.info(f"{self.__class__.__name__} listening on {self.host}:{self.port}")
        server = await websockets.serve(self.handle_new_connection, self.host, self.port)

        try:
            await self.send()
        except asyncio.CancelledError:
            # When the send_message task is cancelled, stop the WebSocket server gracefully
            server.close()
            await server.wait_closed()
            self._logger.info("Server stopped")


async def start_server(address: tuple[str, int], logger: logging.Logger) -> tuple[WSServer, janus.SyncQueue]:
    """ Start the websocket server in isolation.
    """
    messages: janus.Queue[bytes] = janus.Queue()
    server = WSServer(address=address, to_send=messages.async_q, logger=logger)
    return server, messages.sync_q


async def main() -> None:

    def generate_messages(queue: janus.SyncQueue, stop_: threading.Event) -> None:
        while not stop_.is_set():
            json_data = {
                "station": "S160",
                "channel": "HLZ",
                "min": 1.0,
                "max": 2.0,
                "avg": 0.5,
                "trace": [1., 2., 3.]
            }
            msg = json.dumps(json_data)
            queue.put(msg.encode())
            time.sleep(1)
        logger.info("Exiting generate messages")

    logger = get_module_logger("Server", "dev", use_file_handler=False)

    server_address = CONFIG.WS_SERVER_HOST_IP, CONFIG.WS_SERVER_HOST_PORT
    server, messages = await start_server(server_address, logger)

    stop_event = threading.Event()
    thread = threading.Thread(
        target=generate_messages,
        args=(messages, stop_event),
        daemon=True
    )
    thread.start()

    server.add_stop_listener()
    await server.start()

    stop_event.set()
    thread.join()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
