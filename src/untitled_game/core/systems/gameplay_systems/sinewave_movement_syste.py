import math

from untitled_game.core.components.transform_component import TransformComponent
from untitled_game.core.tick_context import TickContext
from untitled_game.core.world.world import EntityId, World


class SineWaveMovementSystem:
    def update(self, world: World, tick_context: TickContext) -> None:
        center_y = 100
        amplitude = 50
        frequency = 0.1

        entities: list[EntityId] = world.query(TransformComponent)
        for entity in entities:
            tranform_comp = world.get_component(entity, TransformComponent)
            if tranform_comp is None:
                continue

            x: int = int(tranform_comp.position.x)
            y: int = int(tranform_comp.position.y)

            x += 1
            y = center_y + amplitude * math.sin(frequency * x)

            tranform_comp.position.x = x
            tranform_comp.position.y = y
