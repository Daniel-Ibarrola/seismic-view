import os
from .config import Config, ProdConfig


if "dev" in os.environ.get("CONFIG", "dev").lower():
    CONFIG = Config()
else:
    CONFIG = ProdConfig()

__version__ = "0.3.0"
