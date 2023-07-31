import asyncio
from socketlib import ServerReceiver
from socketlib.utils.logger import get_module_logger
from typing import Callable, Optional

from seismicview import CONFIG
from seismicview.wsserver import start_server


async def main(
        ws_server_address: tuple[str, int],
        server_receiver_address: tuple[str, int],
        reconnect: bool = False,
        timeout: float = 5, 
        stop: Optional[Callable[[], bool]] = None,
        stop_listener: Optional[Callable] = None
):
    """ Starts a server that expects to receive the data of each station in json format.
        This data is then passed to the Websocket Server, which other websocket clients can
        connect to obtain the data of the desired station.
    """
    if "dev" in CONFIG.NAME:
        use_fh = False
    else:
        use_fh = True

    logger = get_module_logger("Seismic View Server", CONFIG.NAME, use_file_handler=use_fh)
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
        
        ws_server.add_stop_listener(stop_listener)
        await ws_server.start()

        server.shutdown()

    logger.info("Graceful shutdown")
    

if __name__ == "__main__":
    try:
        asyncio.run(main(
            (CONFIG.WS_SERVER_HOST_IP, CONFIG.WS_SERVER_HOST_PORT),
            (CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT)
        ))
    except KeyboardInterrupt:
        pass
