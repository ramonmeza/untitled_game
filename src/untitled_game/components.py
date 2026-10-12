from dataclasses import dataclass, field

from .controller import Controller, GameAction


@dataclass
class BoxComponent:
    width: int
    height: int


@dataclass
class ControllerComponent:
    controller: Controller
    actions: list[GameAction] = field(default_factory=list[GameAction])


@dataclass
class MovementComponent:
    pass


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0
