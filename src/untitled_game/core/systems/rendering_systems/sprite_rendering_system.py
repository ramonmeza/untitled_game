from ...components import SpriteComponent, TransformComponent
from ...renderer import Renderer
from ...tick_context import TickContext
from ...world.world import EntityId, World


class SpriteRenderingSystem:
    def render(self, world: World, tick_context: TickContext, renderer: Renderer) -> None:
        entities: list[EntityId] = world.query(TransformComponent, SpriteComponent)
        for entity in entities:
            tranform_comp = world.get_component(entity, TransformComponent)
            if tranform_comp is None:
                continue

            sprite_comp = world.get_component(entity, SpriteComponent)
            if sprite_comp is None:
                continue

            x: int = int(tranform_comp.position.x)
            y: int = int(tranform_comp.position.y)
            rotation: float = float(tranform_comp.rotation)
            sprite_path = sprite_comp.sprite_path
            renderer.draw_sprite(sprite_path, x, y, rotation)
