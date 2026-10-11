from dataclasses import dataclass, field
from typing import Any, Protocol

from .components import PositionComponent


@dataclass
class Camera:
    position: PositionComponent = field(default_factory=PositionComponent)
    zoom: float = 1.0


@dataclass
class GameAction:
    action: int
    value: Any


class Controller(Protocol):
    """
    Used to connect hardware to the game. Would need an abstraction if we dont want to call raylib directly.
    Will have to think about how to abstract input, but this gives us a hook we could eventually refactor.
    """

    def poll_input(self) -> list[GameAction]: ...
