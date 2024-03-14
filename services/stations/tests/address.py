import os
import random


def get_socket_address() -> tuple[str, int]:
    address = os.environ.get("HOST_DOMAIN_TEST", "localhost")
    return address, random.randint(1024, 49150)

