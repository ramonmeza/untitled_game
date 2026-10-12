from typing import Any

from .camera import Camera
from .components import ActionEmitterComponent, BoxComponent, MovementComponent, PositionComponent
from .ecs import ECS
from .emitters import KeyboardActionEmitter
from .systems import ActionSystem, CameraFollowSystem, MovementSystem


class Game:
    """Manages the ECS and gameplay systems."""

    def __init__(self) -> None:
        self.main_camera: Camera = Camera()
        self.ecs: ECS = ECS()
        self._player_entity_id: int = -1

    def load(self) -> None:
        self._player_entity_id = self._create_player()

    def get_player_entity_id(self) -> int:
        return self._player_entity_id

    def get_action_value(self, entity_id: int, action: int, default: Any = None) -> Any:
        emitter_comps = self.ecs.get_components_of_type(entity_id, ActionEmitterComponent)
        if len(emitter_comps) == 0:
            return None

        emitter_comp = emitter_comps[0]
        value: Any = next(
            (action_item.value for action_item in emitter_comp.actions if action_item.id == action),
            default,
        )
        return value

    def _create_player(self) -> int:
        entity_id: int = self.ecs.create_entity()
        self.ecs.add_component(entity_id, PositionComponent, 250, 10)
        self.ecs.add_component(entity_id, BoxComponent, 200, 100)
        self.ecs.add_component(entity_id, MovementComponent)
        self.ecs.add_component(entity_id, ActionEmitterComponent, KeyboardActionEmitter())
        return entity_id

    def update_systems(self, delta_time: float) -> None:
        # i do a lot filtering of entities by components. probably not optimal, but idk
        player_pos: PositionComponent = self.ecs.get_components_of_type(
            self._player_entity_id, PositionComponent
        )[0]
        emitter_comps: list[ActionEmitterComponent] = self.ecs.get_all_components_of_type(
            ActionEmitterComponent
        )
        ActionSystem.update(emitter_comps)

        movables = self.ecs.get_all_entities_with_components(
            MovementComponent, PositionComponent, ActionEmitterComponent
        )
        MovementSystem.update(self.ecs, movables, delta_time)
        CameraFollowSystem.update(self.main_camera, player_pos, delta_time)

    def tick(self, delta_time: float) -> None:
        self.update_systems(delta_time)
