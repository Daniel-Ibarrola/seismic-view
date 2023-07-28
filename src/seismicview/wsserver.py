import asyncio
import janus
import json
import logging
import signal
from socketlib.utils.logger import get_module_logger
import threading
import time
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
            to_send: janus.AsyncQueue[bytes],
            logger: logging.Logger
    ):
        self.host = address[0]
        self.port = address[1]

        self._to_send = to_send
        self._logger = logger

        self.connections = {}  # type: dict[websockets.WebSocketServerProtocol, str]

    def add_stop_listener(self):
        loop = asyncio.get_event_loop()
        for sig_name in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(getattr(signal, sig_name),
                                    lambda: asyncio.ensure_future(self.stop()))

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
            connections: dict[websockets.WebSocketServerProtocol, str]
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
        station = await ws.recv()
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
        self._logger.info(f"Server listening on {self.host}:{self.port}")
        server = await websockets.serve(self.handle_new_connection, self.host, self.port)

        try:
            await self.send()
        except asyncio.CancelledError:
            # When the send_message task is cancelled, stop the WebSocket server gracefully
            server.close()
            await server.wait_closed()
            self._logger.info("Server stopped")


async def start_server(logger: logging.Logger) -> tuple[WSServer, janus.SyncQueue]:
    """ Start the websocket server in isolation.
    """
    messages: janus.Queue[bytes] = janus.Queue()
    server_address = CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT
    server = WSServer(address=server_address, to_send=messages.async_q, logger=logger)
    return server, messages.sync_q


async def main(stop_event: threading.Thread()) -> None:

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

    server, messages = await start_server(logger)

    thread = threading.Thread(
        target=generate_messages,
        args=(messages, stop_event),
        daemon=True
    )
    thread.start()

    server.add_stop_listener()
    await server.start()


if __name__ == "__main__":
    stop = threading.Event()
    try:
        asyncio.run(main(stop))
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Stopping")
        stop.set()
