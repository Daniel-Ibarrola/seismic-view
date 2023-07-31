import asyncio
import json
from socketlib import ServerSender
from socketlib.utils.logger import get_module_logger
import time
import threading
import pytest
import pytest_asyncio
import random
import websockets as ws

from seismicview.main import main


class TestMain:

    ws_server_address = "localhost", random.randint(1024, 49150)
    client_receiver_address = "localhost", random.randint(1024, 49150)

    @staticmethod
    async def stop_all(stop_event: threading.Event) -> None:
        stop_event.set()
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)
        asyncio.get_event_loop().stop()

    @pytest_asyncio.fixture
    async def ws_server(self):
        stop_event = threading.Event()
        asyncio.ensure_future(
            main(
                ws_server_address=self.ws_server_address,
                client_receiver_address=self.client_receiver_address,
                reconnect=False,
                timeout=1,
                stop=lambda: stop_event.is_set()
            )
        )
        await asyncio.sleep(0.1)  # Give the services some time to start
        yield

        # Cleanup the client and server
        await self.stop_all(stop_event)

    @pytest.fixture
    def server_sender(self) -> ServerSender:
        logger = get_module_logger("ServerSender", "dev", use_file_handler=False)
        server = ServerSender(
            address=self.client_receiver_address,
            reconnect=False,
            timeout=1,
            logger=logger
        )
        server.start()
        time.sleep(0.05)  # give the server some time to start
        yield server

        # Stop the server
        server.shutdown()
        server.close_connection()

    @staticmethod
    def put_messages_in_server(server: ServerSender):
        station1 = {
            "station": "S160",
            "channel": "HLZ",
            "trace": [1, 2, 3, 4]
        }
        station2 = {
            "station": "C166",
            "channel": "HLZ",
            "trace": [1, 2, 3, 4]
        }
        server.to_send.put(json.dumps(station1))
        server.to_send.put(json.dumps(station2))

    @pytest.mark.timeout(5)
    @pytest.mark.asyncio
    async def test_websocket_client_receives_requested_station_data(
            self, server_sender, ws_server,
    ):
        ip, port = self.ws_server_address
        uri = f"ws://{ip}:{port}"
        async with ws.connect(uri) as websocket:
            await websocket.send("S160")
            await asyncio.sleep(0.1)  # give the client some time to connect

            self.put_messages_in_server(server_sender)

            data = await websocket.recv()
            assert json.loads(data) == {
                "station": "S160",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }

    @pytest.mark.timeout(5)
    @pytest.mark.asyncio
    async def test_multiple_clients(
            self, server_sender, ws_server
    ):
        ip, port = self.ws_server_address
        uri = f"ws://{ip}:{port}"
        async with ws.connect(uri) as websocket1, \
                ws.connect(uri) as websocket2:
            await websocket1.send("S160")
            await websocket2.send("C166")
            await asyncio.sleep(0.1)  # give the clients some time to connect

            self.put_messages_in_server(server_sender)

            data1 = await websocket1.recv()
            data2 = await websocket2.recv()

            assert json.loads(data1) == {
                "station": "S160",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }
            assert json.loads(data2) == {
                "station": "C166",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }
