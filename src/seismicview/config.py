import os


class Config:
    NAME = "dev"

    CLIENT_HOST_IP = os.environ.get("CLIENT_HOST_IP", "localhost")
    CLIENT_HOST_PORT = int(os.environ.get("CLIENT_HOST_PORT", 1550))

    SERVER_HOST_IP = os.environ.get("SERVER_HOST_IP", "localhost")
    SERVER_HOST_PORT = int(os.environ.get("SERVER_HOST_PORT", 1550))


class ProdConfig(Config):
    NAME = "prod"
