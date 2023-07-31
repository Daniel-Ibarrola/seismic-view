import asyncio
import janus
import json
import pytest
import pytest_asyncio
import random
import websockets as ws

from seismicview.wsserver import WSServer


class TestServer:
    address = "localhost", random.randint(1024, 49150)

    @pytest_asyncio.fixture()
    async def ws_server(self) -> WSServer:
        queue = janus.Queue()
        server = WSServer(address=self.address, to_send=queue.async_q)
        asyncio.ensure_future(server.start())
        await asyncio.sleep(0.1)  # give the server some time to start
        yield server

        # Cleanup the server
        await server.stop()

    @staticmethod
    async def put_in_queue(server: WSServer) -> None:
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
        await server.to_send.put(json.dumps(station1).encode())
        await server.to_send.put(json.dumps(station2).encode())

    @pytest.mark.timeout(3)
    @pytest.mark.asyncio
    async def test_websocket_client_receives_requested_station_data(self, ws_server):
        uri = f"ws://{self.address[0]}:{self.address[1]}"
        async with ws.connect(uri) as websocket:
            await websocket.send("S160")
            await asyncio.sleep(0.1)  # give the client some time to connect

            await self.put_in_queue(ws_server)

            data = await websocket.recv()
            assert json.loads(data) == {
                "station": "S160",
                "channel": "HLZ",
                "trace": [1, 2, 3, 4]
            }

    @pytest.mark.timeout(3)
    @pytest.mark.asyncio
    async def test_multiple_clients(self, ws_server):
        uri = f"ws://{self.address[0]}:{self.address[1]}"
        async with ws.connect(uri) as websocket1, \
                ws.connect(uri) as websocket2:

            await websocket1.send("S160")
            await websocket2.send("C166")
            await asyncio.sleep(0.1)  # give the clients some time to connect

            await self.put_in_queue(ws_server)

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
