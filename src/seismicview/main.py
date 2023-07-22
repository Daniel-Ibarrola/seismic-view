import asyncio
import janus
from socketlib import ClientReceiver
from socketlib.utils.logger import get_module_logger
from typing import Callable

from seismicview import CONFIG
from seismicview.server import Server


def main(
        reconnect: bool = True, 
        timeout: float = 5, 
        stop: Callable[[], bool] = lambda: False
):
    logger = get_module_logger("Seismic View Server", CONFIG.NAME)

    received: janus.Queue[bytes] = janus.Queue()

    client_address = CONFIG.CLIENT_HOST_IP, CONFIG.CLIENT_HOST_PORT
    client = ClientReceiver(
        address=client_address,
        received=received.sync_q,
        reconnect=reconnect,
        timeout=timeout,
        logger=logger,
        stop=stop
    )

    server_address = CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT
    server = Server(address=server_address, to_send=received.async_q, logger=logger)

    with client:
        client.connect()
        client.start()
        
        server.add_stop_listener()
        try:
            asyncio.run(server.start())
            client.join()
        except KeyboardInterrupt:
            logger.info("Exiting...")
            client.shutdown()
    
    logger.info("Graceful shutdown")
    

if __name__ == "__main__":
    main()
