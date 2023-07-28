import asyncio
import json
import pytest
import pytest_asyncio
import websockets as ws

from seismicview import CONFIG
from seismicview.wsserver import WSServer


class TestServer:

    @pytest_asyncio.fixture()
    async def start_server(self):
        address = CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT
        server = WSServer(address=address)

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
    @pytest.mark.timeout(5)
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
    @pytest.mark.timeout(5)
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
