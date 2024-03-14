import asyncio
from socketlib import ServerReceiver, WatchDog, get_module_logger
from typing import Callable, Optional

from seismicview import CONFIG
from seismicview.wsserver import start_server


async def main(
        ws_server_address: tuple[str, int],
        server_receiver_address: tuple[str, int],
        reconnect: bool = False,
        timeout: Optional[float] = 5,
        stop: Optional[Callable[[], bool]] = None,
        stop_listener: Optional[Callable] = None,
        use_watchdog: bool = False
):
    """ Starts a server that expects to receive the data of each station in json format.
        This data is then passed to the Websocket Server, which other websocket clients can
        connect to obtain the data of the desired station.
    """
    logger = get_module_logger("Seismic View Server", CONFIG.NAME, use_file_handler=False)
    logger.info(f"Server listening in {server_receiver_address}")
    logger.info(f"Websocket Server listening in {ws_server_address}")

    ws_server, messages = await start_server(ws_server_address, logger)
    server = ServerReceiver(
        address=server_receiver_address,
        received=messages,
        reconnect=reconnect,
        timeout=timeout,
        logger=logger,
        stop=stop
    )

    with server:
        server.start()
        if use_watchdog:
            threads = {
                "server_receive": server.receive_thread
            }
            watchdog = WatchDog(threads, logger)
            watchdog.start()
            logger.info(f"Started WatchDog")

        ws_server.add_stop_listener(stop_listener)
        await ws_server.start()

        if use_watchdog:
            watchdog.shutdown()
        server.shutdown()

    logger.info("Graceful shutdown")
    

if __name__ == "__main__":
    try:
        asyncio.run(main(
            (CONFIG.WS_SERVER_HOST_IP, CONFIG.WS_SERVER_HOST_PORT),
            (CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT),
            reconnect=True,
            timeout=None,
            use_watchdog=True
        ))
    except KeyboardInterrupt:
        pass
