from enum import Enum


class EmailStatus(Enum):
    VALID = 0
    IN_USE = 1
    INVALID = 2
