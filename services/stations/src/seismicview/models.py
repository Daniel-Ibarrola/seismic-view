from typing import TypedDict


class Wave(TypedDict):
    station: str
    channel: str
    min: float
    max: float
    avg: float
    trace: list[float]
