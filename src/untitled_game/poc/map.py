from dataclasses import dataclass, field

from .tile import Tile


@dataclass
class Map:
    tiles: list[Tile] = field(default_factory=list[Tile])
    rows: int = 0
    columns: int = 0
