from typing import Protocol

from untitled_game.core.world.world import World

from ..tick_context import TickContext


class GameplaySystem(Protocol):
    def update(self, world: World, tick_context: TickContext) -> None: ...
