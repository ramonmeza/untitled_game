import math
from uuid import uuid4

from .components import BoxComponent, PositionComponent
from .core import Camera, Controller, GameInput, GameState
from .systems import CameraFollowSystem


class Game:
    """Manages the GameState, which is modified by Controllers."""

    def __init__(self) -> None:
        self.main_camera: Camera = Camera()
        self.player_controller: Controller = Controller()
        self.game_state: GameState = GameState()
        self.entities: list[int] = []
        self.position_components: dict[int, PositionComponent] = {}
        self.box_components: dict[int, BoxComponent] = {}

        self.time_since_start: float = 0.0
        self._player_entity_id: int = -1

    def load(self) -> None:
        self.time_since_start = 0.0
        self._player_entity_id = self._create_player()

    def generate_entity_id(self) -> int:
        return uuid4().int

    def _create_player(self) -> int:
        entity_id: int = self.create_entity()
        self.position_components[entity_id] = PositionComponent(250, 10)
        self.box_components[entity_id] = BoxComponent(200, 100)
        return entity_id

    def create_entity(self) -> int:
        entity_id: int = self.generate_entity_id()
        self.entities.append(entity_id)
        return entity_id

    def get_input(self) -> None:
        game_input: GameInput = self.player_controller.poll_input()
        self.game_state.player_input = game_input

    def update_systems(self, delta_time: float) -> None:
        assert self._player_entity_id != -1
        player_pos: PositionComponent = self.position_components[self._player_entity_id]

        # sine movement, should be a component
        sine_amp: float = 200.0
        player_pos.y = math.sin(self.time_since_start) * sine_amp

        CameraFollowSystem.update(self.main_camera, player_pos, delta_time)

    def tick(self, delta_time: float) -> None:
        self.time_since_start += delta_time
        self.get_input()
        self.update_systems(delta_time)
