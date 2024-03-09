# Earthworm AuthClient

Authentication backend for the earthworm grapher app.

## Installation

To install the app for production first clone this repository:

```shell
git clone https://github.com/Daniel-Ibarrola/EwAuth
cd EwAuth
```

Now edit the .env file with the appropriate environment variables. Do the
same with the file in data/emails.txt

Finally, start the container with the app:

```shell
make up
```

Check that it's running with no errors:

```shell
make logs
```

## Developing

### Local environment

To develop in a local environment, first install all dependencies in
a new virtual environment:

```shell
    python -m venv .venv # create a virtual environment
    pip install -r requirements/dev.txt
    pip install -e .
```

Start the development server.

```shell
cd src
export FLASK_APP=ewauth/app.py
flask run
```

Run the tests (on a new terminal). E2E tests require the development server to be running.

```shell
pytest
```

### On Docker

Start the development server

```shell
make dev
```

Run the tests (on a new terminal). The development server must be running.

```shell
make test
```
