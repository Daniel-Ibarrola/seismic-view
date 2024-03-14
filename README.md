# Earthworm Grapher API

API for the earthworm grapher app. It consists of a websocket to stream seismic
data in real time.

## Installation

To install run:

```shell
git clone https://github.com/Daniel-Ibarrola/ew-grapher-api.git
cd ew-grapher-api
make up
```

## Developing

To start a local development environment run the following commands:

```shell
git clone https://github.com/Daniel-Ibarrola/seismic-view.git
cd ew-grapher-api
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
pip install -e .
```

To run the tests:

```shell
pytest
```

Alternatively you can develop and run the tests in a docker container:

```shell
git clone https://github.com/Daniel-Ibarrola/seismic-view.git
cd ew-grapher-api
make build
make dev
make test # run the tests
```
