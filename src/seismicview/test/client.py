""" Server that generates and sends json data for stations.

    Can be used to test the main program.
"""
import json
import logging
import time
from socketlib import ClientSender
from socketlib.basic.send import send_msg
from socketlib.utils.logger import get_module_logger
import sys
from typing import Callable, Optional

from seismicview import CONFIG


STATIONS = {
    # 45 stations
    'AMVM': {'HLZ', 'HLN', 'HLE'},
    'ATVM': {'HLZ', 'HLN', 'HLE'},
    'AZVM': {'HLZ', 'HLN', 'HLE'},
    'C166': {'HL2', 'HLZ', 'HL1'},
    'C266': {'HLZ', 'HL2', 'HL1'},
    'C366': {'HL2', 'HLZ', 'HL1'},
    'CCHA': {'ENN', 'ENZ', 'ENE'},
    'CCHN': {'ENN', 'ENZ', 'ENE'},
    'CCHO': {'ENN', 'ENZ', 'ENE'},
    'CCHS': {'ENN', 'ENZ', 'ENE'},
    'CMAD': {'ENN', 'ENZ', 'ENE'},
    'CRVM': {'HLZ', 'HLN', 'HLE'},
    'CS66': {'HLZ', 'HLN', 'HLE'},
    'D170': {'HL2', 'HLZ', 'HL1'},
    'D270': {'HLZ', 'HL2', 'HL1'},
    'DENP': {'ENN', 'ENZ', 'ENE'},
    'ECTI': {'ENN', 'ENZ', 'ENE'},
    'ENP1': {'ENN', 'ENZ', 'ENE'},
    'ENP2': {'ENN', 'ENZ', 'ENE'},
    'ENP3': {'ENN', 'ENZ', 'ENE'},
    'ENP4': {'ENN', 'ENZ', 'ENE'},
    'ENP5': {'ENN', 'ENZ', 'ENE'},
    'ENP6': {'ENN', 'ENZ', 'ENE'},
    'ENP7': {'ENN', 'ENZ', 'ENE'},
    'ENP8': {'ENN', 'ENZ', 'ENE'},
    'ENP9': {'ENN', 'ENZ', 'ENE'},
    'IERM': {'ENN', 'ENZ', 'ENE'},
    'IGBD': {'ENN', 'ENZ', 'ENE'},
    'IM40': {'HLZ', 'HLN', 'HLE'},
    'IMCS': {'ENN', 'ENZ', 'ENE'},
    'INVM': {'HLZ', 'HLN', 'HLE'},
    'ITFM': {'ENN', 'ENZ', 'ENE'},
    'IXSG': {'ENN', 'ENZ', 'ENE'},
    'MAVM': {'HLZ', 'HLN', 'HLE'},
    'PVIG': {'HHZ', 'HHN', 'HHE'},
    'PZCU': {'ENN', 'ENZ', 'ENE'},
    'S160': {'HL2', 'HLZ', 'HL1'},
    'S260': {'HLZ', 'HL2', 'HL1'},
    'S360': {'HL2', 'HLZ', 'HL1'},
    'SS60': {'HLZ', 'HLN', 'HLE'},
    'TESM': {'ENN', 'ENZ', 'ENE'},
    'TOVM': {'HLZ', 'HLN', 'HLE'},
    'TXVM': {'HLZ', 'HLN', 'HLE'},
    'VTVM': {'HLZ', 'HLN', 'HLE'},
    'ZUVM': {'HLZ', 'HLN', 'HLE'}
}


class WaveClient(ClientSender):

    def __init__(
            self,
            address: tuple[str, int],
            n_stations: int,
            reconnect: bool = True,
            timeout: Optional[float] = None,
            stop: Optional[Callable[[], bool]] = None,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            address=address,
            reconnect=reconnect,
            timeout=timeout,
            stop=stop,
            logger=logger)
        self.stations = self.get_stations(n_stations)

    @staticmethod
    def get_stations(n_stations: int) -> dict[str, set[str]]:
        if n_stations >= len(STATIONS):
            return STATIONS
        else:
            names = list(STATIONS.keys())[:n_stations]
            return {
                st: ch for st, ch in STATIONS.items() if st in names
            }

    def generate_and_send_waves(self) -> None:
        while not self._stop():
            for station, channels in STATIONS.items():
                for ch in channels:
                    wave = {
                        "station": station,
                        "channel":  ch,
                        "min": 1.0,
                        "max": 2.0,
                        "avg": 0.5,
                        "trace": [1., 2., 3.]
                    }
                    msg = json.dumps(wave)
                    error = send_msg(
                        self._socket,
                        msg,
                        self.msg_end,
                        self._logger,
                        "WaveClient"
                    )
                    if error:
                        return
            time.sleep(1)

    def _send(self):
        self._wait_for_connection.wait()
        if self._reconnect:
            while not self._stop_reconnect():
                self.generate_and_send_waves()
                self._connect_to_server()
        else:
            self.generate_and_send_waves()


def main():
    n_stations = len(STATIONS)
    if len(sys.argv) > 1:
        n_stations = int(sys.argv[1])

    logger = get_module_logger("WaveServer", "dev", use_file_handler=False)
    client = WaveClient(
        address=(CONFIG.SERVER_HOST_IP, CONFIG.SERVER_HOST_PORT),
        n_stations=n_stations,
        reconnect=False,
        timeout=5,
        logger=logger
    )

    with client:
        client.connect()
        client.start()

        try:
            client.join()
        except KeyboardInterrupt:
            client.shutdown()

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    main()
