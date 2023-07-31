# Changelog

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