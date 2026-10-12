from typing import Any
from uuid import uuid4

from .camera import Camera
from .components import BoxComponent, ControllerComponent, MovementComponent, PositionComponent
from .controllers import KeyboardController
from .systems import ActionSystem, CameraFollowSystem, MovementSystem


class Game:
    """Manages the ECS and gameplay systems."""

    def __init__(self) -> None:
        self.main_camera: Camera = Camera()
        self.entities: list[int] = []
        self.controller_components: dict[int, ControllerComponent] = {}
        self.position_components: dict[int, PositionComponent] = {}
        self.box_components: dict[int, BoxComponent] = {}
        self.movement_components: dict[int, MovementComponent] = {}
        self._player_entity_id: int = -1

    def load(self) -> None:
        self._player_entity_id = self._create_player()

    def generate_entity_id(self) -> int:
        return uuid4().int

    def get_player_entity_id(self) -> int:
        return self._player_entity_id

    def get_action_value(self, entity_id: int, action: int, default: Any = None) -> Any:
        controller_comp = self.controller_components.get(entity_id, None)
        if controller_comp is None:
            return None
        value: Any = next(
            (
                action_item.value
                for action_item in controller_comp.actions
                if action_item.action == action
            ),
            default,
        )
        return value

    def _create_player(self) -> int:
        entity_id: int = self.create_entity()
        self.position_components[entity_id] = PositionComponent(250, 10)
        self.box_components[entity_id] = BoxComponent(200, 100)
        self.movement_components[entity_id] = MovementComponent()
        self.controller_components[entity_id] = ControllerComponent(KeyboardController())
        return entity_id

    def create_entity(self) -> int:
        entity_id: int = self.generate_entity_id()
        self.entities.append(entity_id)
        return entity_id

    def update_systems(self, delta_time: float) -> None:
        player_pos: PositionComponent = self.position_components[self._player_entity_id]
        ActionSystem.update(self.controller_components)
        MovementSystem.update(
            self.movement_components,
            self.position_components,
            self.controller_components,
            delta_time,
        )
        CameraFollowSystem.update(self.main_camera, player_pos, delta_time)

    def tick(self, delta_time: float) -> None:
        self.update_systems(delta_time)
