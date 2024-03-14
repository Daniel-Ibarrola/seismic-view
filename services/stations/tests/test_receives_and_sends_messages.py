import asyncio
import json
from socketlib import ClientSender
from socketlib.utils.logger import get_module_logger
import threading
import pytest
import pytest_asyncio
import websockets as ws

from seismicview.main import main
from address import get_socket_address


class TestMain:

    ws_server_address = get_socket_address()
    server_receiver_address = get_socket_address()

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
        """ Starts the websocket and receiver servers."""
        logger = get_module_logger("WSServer", "dev", use_file_handler=False)
        logger.info(f"Starting WS Server with address: {self.ws_server_address}")
        logger.info(f"Starting Server Receiver with address: {self.server_receiver_address}")

        stop_event = threading.Event()
        asyncio.ensure_future(
            main(
                ws_server_address=self.ws_server_address,
                server_receiver_address=self.server_receiver_address,
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
    def client_sender(self) -> ClientSender:
        """ Start the client that will send data to the server receiver.
        """
        logger = get_module_logger("ClientSender", "dev", use_file_handler=False)
        logger.info(f"Starting client sender, address: {self.server_receiver_address}")

        client = ClientSender(
            address=self.server_receiver_address,
            reconnect=False,
            timeout=1,
            logger=logger
        )
        yield client

        # Stop the server
        try:
            client.shutdown()
        except RuntimeError:
            pass

        client.close_connection()

    @staticmethod
    def put_messages_in_client(client: ClientSender):
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
        client.to_send.put(json.dumps(station1))
        client.to_send.put(json.dumps(station2))

    @pytest.mark.timeout(5)
    @pytest.mark.asyncio
    async def test_multiple_clients_connect_and_receive_data_from_requested_station(
            self, client_sender, ws_server
    ):
        client_sender.connect()
        client_sender.start()

        ip, port = self.ws_server_address
        uri = f"ws://{ip}:{port}"
        async with ws.connect(uri) as websocket1, \
                ws.connect(uri) as websocket2:
            await websocket1.send("S160")
            await websocket2.send("C166")
            await asyncio.sleep(0.1)  # give the clients some time to connect

            self.put_messages_in_client(client_sender)

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
