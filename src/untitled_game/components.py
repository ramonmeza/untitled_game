from dataclasses import dataclass, field

from .controller import Controller, GameAction


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@dataclass
class BoxComponent:
    width: int
    height: int


@dataclass
class MovementComponent:
    pass


@dataclass
class ControllerComponent:
    controller: Controller
    actions: list[GameAction] = field(default_factory=list[GameAction])
