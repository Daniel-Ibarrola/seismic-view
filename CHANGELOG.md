# Changelog

## v0.3.4 (11/08/2022)
- Updated pysocklib to 0.3.4 fixing server reconnection errors
- Removed custom network from development config.

## v0.3.3 (9/08/2022)
- Removed custom network from production deployment leading to errors.
- Removed logger file handler.

## v0.3.2 (7/08/2023)
- Make file updated with commands description
- Docker containers use custom names
- Docker image custom name

## v0.3.1 (7/08/2023)
Updated default ports so that the test client can connect to the main program.

## v0.3.0 (1/08/2023)

- Containers use a custom network
- Added arg parser to `ws_client.py` 

## v0.2.0 (31/07/2023)

### Features

- Main program now uses a socket server to receive the station data instead
of a client requesting it. 

- Updated test program "server.py" to be a client and renamed it to "client.py"
- Docker image and docker compose file to run the program in a container.


## v0.1.0 (31/07/2023)

First release. Main program is a websocket server that can
send seismic station data to all connected clients. At the same
time it receives the seismic station data from another server to which
it connects.

### Tests

End to end and unit tests have been implemented with pytest.

Programs to do manual tests are found in the test module. It consists of
a server that generates and sends seismic data and a websocket client.

### CI

Continuous Integration with GitHub actions.