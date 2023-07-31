# Changelog

## v0.1.0

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