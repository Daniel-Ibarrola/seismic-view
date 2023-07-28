""" Websocket client that receives data periodically
"""
import asyncio
import websockets as ws
import sys
import signal


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
    print("Starting Client")

    if len(sys.argv) > 1:
        station = sys.argv[1]
    else:
        raise ValueError("Must pass a station as argument")

    uri = "ws://localhost:1550"
    async for client in ws.connect(uri):
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
