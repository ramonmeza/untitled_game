"""
Actions
An action something the player can do to influence the game. We define all the actions a player can
take, and each frame we can query an emitter object for Actions the game should take. The emitter
will return the Actions, which includes the value to set the action to. Systems can depend on
actions instead of input devices or emitters directly.
"""

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any, Protocol


class ActionID(IntEnum):
    """All of the actions a player can take to affect the game."""

    ACCELERATE = auto()
    BRAKE = auto()
    EBRAKE = auto()
    STEERING = auto()
    ACTIVATE = auto()


@dataclass
class ActionValue:
    """Maps an ActionID to an arbitrary value."""

    id: ActionID
    value: Any


class ActionEmitter(Protocol):
    """Can be polled to get a list of desired Actions to execute."""

    def poll_actions(self) -> list[ActionValue]: ...
