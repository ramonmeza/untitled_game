from dataclasses import dataclass, field

from .. import Vector2
from .enums import (
    ControllerAnalogInputs,
    ControllerAxis,
    ControllerDigitalInputs,
    KeyboardKey,
    MouseButton,
)


@dataclass
class ControllerState:
    axes: list[Vector2] = field(default_factory=lambda: [Vector2(0, 0)] * len(ControllerAxis))
    analog_inputs: list[float] = field(default_factory=lambda: [0.0] * len(ControllerAnalogInputs))
    digital_inputs: list[bool] = field(
        default_factory=lambda: [False] * len(ControllerDigitalInputs)
    )


@dataclass
class KeyboardState:
    keys: list[bool] = field(default_factory=lambda: [False] * len(KeyboardKey))


@dataclass
class MouseState:
    buttons: list[bool] = field(default_factory=lambda: [False] * len(MouseButton))
    position: Vector2 = field(default_factory=Vector2)
    scroll: Vector2 = field(default_factory=Vector2)


@dataclass
class InputState:
    controller_state: ControllerState = field(default_factory=ControllerState)
    keyboard_state: KeyboardState = field(default_factory=KeyboardState)
    mouse_state: MouseState = field(default_factory=MouseState)
