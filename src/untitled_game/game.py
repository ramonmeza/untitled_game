from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .components import BoxComponent, MovementComponent, PositionComponent
from .controllers import KeyboardController
from .core import Camera, Controller, GameAction
from .systems import CameraFollowSystem, MovementSystem


@dataclass
class GameState:
    """Mutable values for the game."""

    player_inputs: list[GameAction] = field(default_factory=list[GameAction])

    def get_player_input_value(self, action: int) -> Any:
        return next(
            (game_input.value for game_input in self.player_inputs if game_input.action == action),
            0,
        )


class Game:
    """Manages the GameState, which is modified by Controllers."""

    def __init__(self) -> None:
        self.main_camera: Camera = Camera()
        self.player_controller: Controller = KeyboardController()
        self.game_state: GameState = GameState()
        self.entities: list[int] = []
        self.position_components: dict[int, PositionComponent] = {}
        self.box_components: dict[int, BoxComponent] = {}
        self.movement_components: dict[int, MovementComponent] = {}

        self._player_entity_id: int = -1

    def load(self) -> None:
        self._player_entity_id = self._create_player()

    def generate_entity_id(self) -> int:
        return uuid4().int

    def _create_player(self) -> int:
        entity_id: int = self.create_entity()
        self.position_components[entity_id] = PositionComponent(250, 10)
        self.box_components[entity_id] = BoxComponent(200, 100)
        self.movement_components[entity_id] = MovementComponent()
        return entity_id

    def create_entity(self) -> int:
        entity_id: int = self.generate_entity_id()
        self.entities.append(entity_id)
        return entity_id

    def get_input(self) -> None:
        player_inputs: list[GameAction] = self.player_controller.poll_input()
        self.game_state.player_inputs = player_inputs

    def update_systems(self, delta_time: float) -> None:
        assert self._player_entity_id != -1
        player_pos: PositionComponent = self.position_components[self._player_entity_id]
        MovementSystem.update(self.movement_components, self.position_components, delta_time)
        CameraFollowSystem.update(self.main_camera, player_pos, delta_time)

    def tick(self, delta_time: float) -> None:
        self.get_input()
        self.update_systems(delta_time)
