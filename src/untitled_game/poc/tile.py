from enum import IntEnum, auto


class Tile(IntEnum):
    ROAD = auto()
    GRASS = auto()
    DIRT = auto()
    BARRIER = auto()
