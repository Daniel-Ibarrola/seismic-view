import asyncio
from socketlib import ClientReceiver
from socketlib.utils.logger import get_module_logger
from typing import Callable, Optional

from seismicview import CONFIG
from seismicview.wsserver import start_server


async def main(
        ws_server_address: tuple[str, int],
        client_receiver_address: tuple[str, int],
        reconnect: bool = True, 
        timeout: float = 5, 
        stop: Optional[Callable[[], bool]] = None,
        stop_listener: Optional[Callable] = None
):
    if "dev" in CONFIG.NAME:
        use_fh = False
    else:
        use_fh = True

    logger = get_module_logger("Seismic View Server", CONFIG.NAME, use_file_handler=use_fh)
    server, messages = await start_server(ws_server_address, logger)
    client = ClientReceiver(
        address=client_receiver_address,
        received=messages,
        reconnect=reconnect,
        timeout=timeout,
        logger=logger,
        stop=stop
    )

    with client:
        client.connect()
        client.start()
        
        server.add_stop_listener(stop_listener)
        await server.start()

        client.shutdown()

    logger.info("Graceful shutdown")
    

if __name__ == "__main__":
    try:
        asyncio.run(main(
            (CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT),
            (CONFIG.CLIENT_HOST_IP, CONFIG.CLIENT_HOST_PORT)
        ))
    except KeyboardInterrupt:
        pass
