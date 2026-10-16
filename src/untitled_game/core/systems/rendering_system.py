from typing import Protocol

from ..renderer import Renderer
from ..tick_context import TickContext
from ..world.world import World


class RenderingSystem(Protocol):
    def render(self, world: World, tick_context: TickContext, renderer: Renderer) -> None: ...
