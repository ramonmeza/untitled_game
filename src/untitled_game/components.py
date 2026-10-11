from dataclasses import dataclass


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@dataclass
class BoxComponent:
    width: int
    height: int


@dataclass
class SineMovementComponent:
    pass
