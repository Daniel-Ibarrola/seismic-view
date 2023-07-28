import asyncio
import json
from socketlib import ServerSender
from socketlib.utils.logger import get_module_logger
import time
import threading
import pytest
import pytest_asyncio
import websockets as ws

from seismicview import CONFIG
from seismicview.main import main


async def stop_all(stop_event: threading.Event) -> None:
    stop_event.set()
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_event_loop().stop()


@pytest_asyncio.fixture()
async def start_client_receiver_and_websocket_server():
    stop_event = threading.Event()
    asyncio.ensure_future(main(False, 0.1, lambda: stop_event.is_set()))
    await asyncio.sleep(0.1)  # Give the services some time to start
    yield

    # Cleanup the client and server
    stop_event.set()
    await stop_all(stop_event)


@pytest.fixture()
def start_server_sender():
    logger = get_module_logger("ServerSender", "dev", use_file_handler=False)
    server = ServerSender(
        address=(CONFIG.CLIENT_HOST_IP, CONFIG.CLIENT_HOST_PORT),
        reconnect=False,
        timeout=0.1,
        logger=logger
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
