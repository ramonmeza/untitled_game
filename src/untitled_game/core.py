from dataclasses import dataclass, field

import pyray as raylib

from .components import PositionComponent
from .utils import clamp


class GameInput:
    """Represents inputs used to modify the state of the game."""

    def __init__(self) -> None:
        self._accelerator: float = 0.0
        self._brake: float = 0.0
        self._ebrake: float = 0.0
        self._steering: float = 0.0
        self._activate: bool = False

    def __str__(self) -> str:
        attrs: list[str] = [
            f"{attr.removeprefix('_')}={getattr(self, attr.removeprefix('_'))!s}"
            for attr in vars(self)
        ]
        return f"<GameInput {' '.join(attrs)}>"

    @property
    def accelerator(self) -> float:
        return self._accelerator

    @accelerator.setter
    def accelerator(self, value: float) -> None:
        self._accelerator = clamp(value, 0, 1)

    @property
    def brake(self) -> float:
        return self._brake

    @brake.setter
    def brake(self, value: float) -> None:
        self._brake = clamp(value, 0, 1)

    @property
    def ebrake(self) -> float:
        return clamp(self._ebrake, 0, 1)

    @ebrake.setter
    def ebrake(self, value: float) -> None:
        self._ebrake = clamp(value, 0, 1)

    @property
    def steering(self) -> float:
        return self._steering

    @steering.setter
    def steering(self, value: float) -> None:
        self._steering = clamp(value, -1, 1)

    @property
    def activate(self) -> bool:
        return self._activate

    @activate.setter
    def activate(self, value: bool) -> None:
        self._activate = value


@dataclass
class GameState:
    """Mutable values for the game."""

    player_input: GameInput = field(default_factory=GameInput)


@dataclass
class Camera:
    position: PositionComponent = field(default_factory=PositionComponent)
    zoom: float = 1.0


class Controller:
    """
    Used to connect hardware to the game. Would need an abstraction if we dont want to call raylib directly.
    Will have to think about how to abstract input, but this gives us a hook we could eventually refactor.
    """

    def poll_input(self) -> GameInput:
        game_input: GameInput = GameInput()

        game_input.accelerator = float(raylib.is_key_down(raylib.KeyboardKey.KEY_W))
        game_input.brake = float(raylib.is_key_down(raylib.KeyboardKey.KEY_S))
        game_input.ebrake = float(raylib.is_key_down(raylib.KeyboardKey.KEY_SPACE))

        game_input.steering = 0.0  # recenter, wouldnt be necessary with analog stick
        steer_left: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_A) else 0
        steer_right: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_D) else 0
        steering: float = steer_right - steer_left
        game_input.steering = steering

        game_input.activate = raylib.is_key_down(raylib.KeyboardKey.KEY_E)

        return game_input
