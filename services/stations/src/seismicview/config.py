import os


class Config:
    NAME = "dev"

    # Address from which the server connects to receive information
    SERVER_HOST_IP = os.environ.get("SERVER_HOST_IP", "localhost")
    SERVER_HOST_PORT = int(os.environ.get("SERVER_HOST_PORT", 13342))

    # Address of the websocket server
    WS_SERVER_HOST_IP = os.environ.get("WS_SERVER_HOST_IP", "localhost")
    WS_SERVER_HOST_PORT = int(os.environ.get("WS_SERVER_HOST_PORT", 13345))


class ProdConfig(Config):
    NAME = "prod"
