import json
from socketlib import ServerSender
import time
import threading
import pytest
import pytest_asyncio
import websockets as ws

from seismicview import CONFIG
from seismicview.server import WSServer
from seismicview.main import main


@pytest_asyncio.fixture()
async def start_client_receiver_and_websocket_server():
    stop_event = threading.Event()
    thread = threading.Thread(
        target=main,
        args=(False, 0.1, lambda: not stop_event.is_set())
    )
    thread.start()
    time.sleep(0.1)  # give the client and server some time to start
    yield

    # Cleanup the client and server
    stop_event.set()
    await WSServer.stop()
    thread.join()


@pytest.fixture()
def start_server_sender():
    server = ServerSender(
        address=(CONFIG.CLIENT_HOST_IP, CONFIG.CLIENT_HOST_PORT),
        reconnect=False,
        timeout=0.1,
    )
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
    server.start()
    time.sleep(0.1)  # give the server some time to start
    yield

    # Stop the server
    server.shutdown()
    server.close_connection()


@pytest.mark.usefixtures("start_client_receiver_and_websocket_server")
@pytest.mark.usefixtures("start_server_sender")
@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_websocket_client_receives_requested_station_data():
    uri = f"ws://{CONFIG.SERVER_HOST_IP}:{CONFIG.SERVER_HOST_PORT}"
    async with ws.connect(uri) as websocket:
        await websocket.send("S160")
        data = await websocket.recv()
        assert json.loads(data) == {
            "name": "C166",
            "channel": "HLZ",
            "trace": [1, 2, 3, 4]
        }


@pytest.mark.usefixtures("start_client_receiver_and_websocket_server")
@pytest.mark.usefixtures("start_server_sender")
@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_multiple_clients():
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
