from ..renderer import Renderer
from ..systems import GameplaySystem, RenderingSystem
from ..systems.rendering_systems import SpriteRenderingSystem
from ..tick_context import TickContext
from .world import World


class WorldRunner:
    def __init__(self, world: World) -> None:
        self._gameplay_systems: list[GameplaySystem] = []
        self._rendering_systems: list[RenderingSystem] = [SpriteRenderingSystem()]
        self._world: World = world

    @property
    def rendering_systems(self) -> list[RenderingSystem]:
        return self._rendering_systems

    def tick(self, tick_context: TickContext) -> None:
        for system in self._gameplay_systems:
            system.update(tick_context)

    def render(self, tick_context: TickContext, renderer: Renderer) -> None:
        renderer.begin_frame()
        for system in self._rendering_systems:
            system.render(self._world, tick_context, renderer)
        renderer.end_frame()
