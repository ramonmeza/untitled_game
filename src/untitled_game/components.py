from dataclasses import dataclass
from enum import IntEnum, auto


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@dataclass
class BoxComponent:
    width: int
    height: int


class MovementStyle(IntEnum):
    SINE = auto()


@dataclass
class MovementComponent:
    movement_style: MovementStyle = MovementStyle.SINE
