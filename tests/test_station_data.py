import json
import pytest
from seismicview.wsserver import WSServer


class FakeWebsocket:

    def __init__(self):
        self.sent = []  # type: list[str]

    async def send(self, msg: str):
        self.sent.append(msg)

    def __hash__(self):
        return id(self)


class TestSendStationData:

    @pytest.mark.asyncio
    async def test_does_not_send_non_requested_station(self):
        websocket1 = FakeWebsocket()
        websocket2 = FakeWebsocket()

        connections = {
            websocket1: "S160",
            websocket2: "C166",
        }

        data = json.dumps({
            "station": "D170",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        }).encode()

        await WSServer.send_station_data(data, connections)
        assert len(websocket1.sent) == 0
        assert len(websocket2.sent) == 0

    @pytest.mark.asyncio
    async def test_sends_only_requested_station(self):
        websocket1 = FakeWebsocket()
        websocket2 = FakeWebsocket()

        connections = {
            websocket1: "S160",
            websocket2: "C166",
        }

        data = {
            "station": "S160",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        }
        json_data = json.dumps(data).encode()

        await WSServer.send_station_data(json_data, connections)

        assert len(websocket1.sent) == 1
        assert len(websocket2.sent) == 0

        sent_data = websocket1.sent[0]
        assert json.loads(sent_data) == data

    @pytest.mark.asyncio
    async def test_multiple_clients_request_same_station(self):
        websocket1 = FakeWebsocket()
        websocket2 = FakeWebsocket()

        connections = {
            websocket1: "S160",
            websocket2: "S160",
        }

        data = {
            "station": "S160",
            "channel": "HLZ",
            "trace": [4, 5, 6]
        }
        json_data = json.dumps(data).encode()

        await WSServer.send_station_data(json_data, connections)
        assert len(websocket1.sent) == 1
        assert len(websocket2.sent) == 1

        assert json.loads(websocket1.sent[0]) == data
        assert json.loads(websocket2.sent[0]) == data
