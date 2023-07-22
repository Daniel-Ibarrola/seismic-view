import asyncio
import json
import pytest
import pytest_asyncio
import websockets as ws

from seismicview import CONFIG
from seismicview.server import Server


class TestServer:

    @pytest_asyncio.fixture()
    async def start_server(self):
        address = CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT
        server = Server(address=address)

        station1 = {
            "name": "S160",
            "channel": "HLZ",
            "trace": [1, 2, 3, 4]
        }
        station2 = {
            "name": "C166",
            "channel": "HLZ",
            "trace": [1, 2, 3, 4]
        }
        server.to_send.put(json.dumps(station1))
        server.to_send.put(json.dumps(station2))

        asyncio.ensure_future(server.start())
        await asyncio.sleep(0.1)  # give the server some time to start
        yield

        # Cleanup the client and server
        await server.stop()

    @pytest.mark.usefixtures("start_server")
    @pytest.mark.asyncio
    async def test_websocket_client_receives_requested_station_data(self):
        uri = f"ws://{CONFIG.SERVER_HOST_IP}:{CONFIG.SERVER_HOST_PORT}"
        async with ws.connect(uri) as websocket:
            await websocket.send("S160")
            data = await websocket.recv()
            assert json.loads(data) == {
                "name": "C166",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }
    
    @pytest.mark.usefixtures("start_server")
    @pytest.mark.asyncio
    async def test_multiple_clients(self):
        uri = f"ws://{CONFIG.SERVER_HOST_IP}:{CONFIG.SERVER_HOST_PORT}"
        async with ws.connect(uri) as websocket1, \
                ws.connect(uri) as websocket2:

            await websocket1.send("S160")
            await websocket2.send("C166")

            data1 = await websocket1.recv()
            data2 = await websocket2.recv()

            assert json.loads(data1) == {
                "name": "S160",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }
            assert json.loads(data2) == {
                "name": "C166",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }


class FakeWebsocket:

    def __init__(self):
        self.sent = []

    def send(self, msg: str):
        self.sent.append(msg)


class TestSendStationData:

    def test_does_not_send_non_requested_station(self):
        websocket1 = FakeWebsocket(name="test1")
        websocket2 = FakeWebsocket(name="test2")

        connections = {
            websocket1: "S160",
            websocket2: "C166",
        }

        data = json.dumps({
            "name": "D170",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        }).encode()

        Server.send_station_data(data, connections)
        assert len(websocket1.sent) == 0
        assert len(websocket2.sent) == 0

    def test_sends_only_requested_station(self):
        websocket1 = FakeWebsocket(name="test1")
        websocket2 = FakeWebsocket(name="test2")

        connections = {
            websocket1: "S160",
            websocket2: "C166",
        }

        data = json.dumps({
            "name": "S160",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        })
        encoded_data = data.encode()

        Server.send_station_data(encoded_data, connections)

        assert len(websocket1.sent) == 1
        assert len(websocket2.sent) == 0

        data = websocket1.sent[0]
        assert json.loads(data) == data

    def test_multiple_clients_request_same_station(self):
        websocket1 = FakeWebsocket(name="test1")
        websocket2 = FakeWebsocket(name="test2")

        connections = {
            websocket1: "S160",
            websocket2: "S160",
        }

        data = json.dumps({
            "name": "S160",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        })
        encoded_data = data.encode()

        Server.send_station_data(encoded_data, connections)
        assert len(websocket1.sent) == 1
        assert len(websocket2.sent) == 1

        assert json.loads(websocket1.sent[0]) == data
        assert json.loads(websocket2.sent[0]) == data
