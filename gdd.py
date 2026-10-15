from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Protocol, override

import pyray as raylib


class ZeroBasedIntEnum(IntEnum):
    @override
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
        return count


class Key(ZeroBasedIntEnum):
    ESCAPE = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    TILDE = auto()
    NUMBER_1 = auto()
    NUMBER_2 = auto()
    NUMBER_3 = auto()
    NUMBER_4 = auto()
    NUMBER_5 = auto()
    NUMBER_6 = auto()
    NUMBER_7 = auto()
    NUMBER_8 = auto()
    NUMBER_9 = auto()
    NUMBER_0 = auto()
    MINUS = auto()
    EQUAL = auto()
    BACKSPACE = auto()
    TAB = auto()
    Q = auto()
    W = auto()
    E = auto()
    R = auto()
    T = auto()
    Y = auto()
    U = auto()
    I = auto()
    O = auto()
    P = auto()
    LEFT_SQUARE_BRACKET = auto()
    RIGHT_SQUARE_BRACKET = auto()
    BACKSLASH = auto()
    CAPS_LOCK = auto()
    A = auto()
    S = auto()
    D = auto()
    F = auto()
    G = auto()
    H = auto()
    J = auto()
    K = auto()
    L = auto()
    SEMICOLON = auto()
    SINGLE_QUOTE = auto()
    RIGHT_ENTER = auto()
    LEFT_SHIFT = auto()
    Z = auto()
    X = auto()
    C = auto()
    V = auto()
    B = auto()
    N = auto()
    M = auto()
    COMMA = auto()
    PERIOD = auto()
    FORWARD_SLASH = auto()
    RIGHT_SHIFT = auto()
    LEFT_CTRL = auto()
    OS_KEY = auto()
    LEFT_ALT = auto()
    SPACE = auto()
    RIGHT_ALT = auto()
    OPTION_KEY = auto()
    RIGHT_CTRL = auto()
    PRINT_SCREEN = auto()
    SCREEN_LOCK = auto()
    PAUSE = auto()
    INSERT = auto()
    HOME = auto()
    PAGE_UP = auto()
    DELETE = auto()
    END = auto()
    PAGE_DOWN = auto()
    ARROW_UP = auto()
    ARROW_LEFT = auto()
    ARROW_DOWN = auto()
    ARROW_RIGHT = auto()


class MouseButton(ZeroBasedIntEnum):
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    SCROLL_WHEEL = auto()
    FORWARD = auto()
    BACK = auto()


class ControllerAxis(ZeroBasedIntEnum):
    LEFT_STICK = auto()
    RIGHT_STICK = auto()


class ControllerAnalogInputs(ZeroBasedIntEnum):
    LEFT_TRIGGER = auto()
    RIGHT_TRIGGER = auto()


class ControllerDigitalInputs(ZeroBasedIntEnum):
    LB = auto()
    RB = auto()

    LEFT_STICK = auto()
    RIGHT_STICK = auto()

    KEYPAD_UP = auto()
    KEYPAD_DOWN = auto()
    KEYPAD_LEFT = auto()
    KEYPAD_RIGHT = auto()

    SELECT = auto()
    PAUSE = auto()
    SHARE = auto()

    FACE_TOP = auto()
    FACE_BOTTOM = auto()
    FACE_LEFT = auto()
    FACE_RIGHT = auto()


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0


@dataclass
class ControllerState:
    axes: list[Vector2] = field(default_factory=lambda: [Vector2(0, 0)] * len(ControllerAxis))
    analog_inputs: list[float] = field(default_factory=lambda: [0.0] * len(ControllerAnalogInputs))
    digital_inputs: list[bool] = field(
        default_factory=lambda: [False] * len(ControllerDigitalInputs)
    )


@dataclass
class KeyboardState:
    keys: list[bool] = field(default_factory=lambda: [False] * len(Key))


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


class InputSource(Protocol):
    def poll(self, state: InputState) -> None: ...


class RaylibInputSource:
    def _update_controller_state(self, state: ControllerState) -> None:
        # modify controller_state here
        pass

    def _update_keyboard_state(self, state: KeyboardState) -> None:
        # modify keyboard_state here
        state.keys[Key.W] = raylib.is_key_down(raylib.KeyboardKey.KEY_W)

    def _update_mouse_state(self, state: MouseState) -> None:
        # modify mouse_state here
        pass

    def get_input_state(self, state: InputState) -> None:
        self._update_controller_state(state.controller_state)
        self._update_keyboard_state(state.keyboard_state)
        self._update_mouse_state(state.mouse_state)


class InputHandler:
    def __init__(self, input_source: InputSource) -> None:
        self._input_source: InputSource = input_source
        self._input_state: InputState = InputState()

    def get_input_state(self) -> InputState:
        return self._input_state

    def poll(self) -> None:
        self._input_source.poll(self._input_state)


if __name__ == "__main__":
    raylib.init_window(400, 400, "keyboard test")

    input_handler = InputHandler(RaylibInputSource())
    while not input_handler.get_input_state().keyboard_state.keys[Key.W]:
        input_handler.poll()

        # hook for example purposes
        raylib.begin_drawing()
        raylib.clear_background(raylib.BLACK)
        raylib.end_drawing()
