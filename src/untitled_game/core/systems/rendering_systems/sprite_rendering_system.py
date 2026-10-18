from typing import cast

from ...components import SpriteComponent, TransformComponent
from ...renderer import Renderer
from ...tick_context import TickContext
from ...world.world import EntityId, World


class SpriteRenderingSystem:
    def render(self, world: World, tick_context: TickContext, renderer: Renderer) -> None:
        entities: list[EntityId] = world.query_by_component_types(
            TransformComponent, SpriteComponent
        )
        for entity in entities:
            tranform_comp = cast(
                TransformComponent, world.get_component_by_type(entity, TransformComponent)
            )
            sprite_comp = cast(
                SpriteComponent, world.get_component_by_type(entity, SpriteComponent)
            )
            x: int = int(tranform_comp.position.x)
            y: int = int(tranform_comp.position.y)
            sprite_path = sprite_comp.sprite_path
            renderer.draw_sprite(sprite_path, x, y)
