""" Websocket client that receives data periodically.

    Can be used to test the main program.
"""
import argparse
import asyncio
import websockets as ws
import signal


def parse_args():
    parser = argparse.ArgumentParser(
        description="Websocket client to test the SeismicView's websocket server")
    parser.add_argument(
        "--ip",
        "-i",
        type=str,
        default="localhost",
        help="The ip where the client will connect"
             " (default localhost)."
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=12345,
        help="The port where the client will connect"
             " (default 12345)."
    )
    parser.add_argument(
        "--station",
        "-s",
        default="S160",
        help="Name of the station this client will request"
             " (default 'S160')"
    )
    args = parser.parse_args()
    return args.ip, args.port, args.station


async def receive(
        websocket: ws.WebSocketCommonProtocol,
        station: str) -> None:
    """ Receive messages from the server indefinitely"""
    await websocket.send(station)
    while True:
        data = await websocket.recv()
        print(data)


def stop_client_on_keyboard_interrupt():
    loop = asyncio.get_event_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame),
                                lambda: asyncio.ensure_future(stop_client()))


async def stop_client():
    print("\nStopping WebSocket Client...")
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_event_loop().stop()


async def main():
    """ Starts a websocket client that will receive data from the requested station.
    """
    ip, port, station = parse_args()

    uri = f"ws://{ip}:{port}"
    async for client in ws.connect(uri):
        print(f"Client connected to {uri}")
        try:
            await receive(client, station)
        except ws.ConnectionClosed:
            await asyncio.sleep(1)
            continue
        except asyncio.CancelledError:
            await client.close()
            break

    print("Websocket Client stopped gracefully")


if __name__ == "__main__":
    stop_client_on_keyboard_interrupt()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
