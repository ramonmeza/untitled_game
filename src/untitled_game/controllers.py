import pyray as raylib

from .actions import Actions
from .controller import GameAction


class KeyboardController:
    def poll_actions(self) -> list[GameAction]:
        steer_left: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_A) else 0
        steer_right: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_D) else 0
        steering: float = steer_right - steer_left
        return [
            GameAction(Actions.ACCELERATE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_W))),
            GameAction(Actions.BRAKE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_S))),
            GameAction(Actions.EBRAKE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_SPACE))),
            GameAction(Actions.STEERING, steering),
            GameAction(Actions.ACTIVATE, raylib.is_key_down(raylib.KeyboardKey.KEY_E)),
        ]
