import json
import websockets


class Server:
    """A websocket server that can send data continuously to multiple clients.
    """
    @staticmethod
    async def send_station_data(
            data: bytes,
            connections: dict[websockets.WebSocketClientProtocol, str]
    ):
        if connections:
            data_str = data.decode()
            data_json = json.loads(data_str)
            current_station = data_json["name"]
            for ws, station in connections.items():
                if station == current_station:
                    await ws.send(data_str)
