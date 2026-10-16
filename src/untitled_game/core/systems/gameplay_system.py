from typing import Protocol

from ..tick_context import TickContext


class GameplaySystem(Protocol):
    def update(self, tick_context: TickContext) -> None: ...
