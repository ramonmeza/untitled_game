import pyray as raylib

from .actions import ActionID, ActionValue


class KeyboardActionEmitter:
    def poll_actions(self) -> list[ActionValue]:
        steer_left: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_A) else 0
        steer_right: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_D) else 0
        steering: float = steer_right - steer_left
        return [
            ActionValue(ActionID.ACCELERATE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_W))),
            ActionValue(ActionID.BRAKE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_S))),
            ActionValue(ActionID.EBRAKE, float(raylib.is_key_down(raylib.KeyboardKey.KEY_SPACE))),
            ActionValue(ActionID.STEERING, steering),
            ActionValue(ActionID.ACTIVATE, raylib.is_key_down(raylib.KeyboardKey.KEY_E)),
        ]
