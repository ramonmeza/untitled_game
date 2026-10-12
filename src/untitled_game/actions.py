from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any


@dataclass
class GameAction:
    action: int
    value: Any


class Actions(IntEnum):
    ACCELERATE = auto()
    BRAKE = auto()
    EBRAKE = auto()
    STEERING = auto()
    ACTIVATE = auto()
