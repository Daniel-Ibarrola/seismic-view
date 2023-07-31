import os


class Config:
    NAME = "dev"

    # Address to which the client connects to receive information
    CLIENT_HOST_IP = os.environ.get("CLIENT_HOST_IP", "localhost")
    CLIENT_HOST_PORT = int(os.environ.get("CLIENT_HOST_PORT", 1551))

    # Address of the websocket server
    SERVER_HOST_IP = os.environ.get("SERVER_HOST_IP", "localhost")
    SERVER_HOST_PORT = int(os.environ.get("SERVER_HOST_PORT", 1552))


class ProdConfig(Config):
    NAME = "prod"
