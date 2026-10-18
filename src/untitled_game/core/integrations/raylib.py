import pyray as raylib

from ..input import (
    ControllerState,
    InputState,
    KeyboardKey,
    KeyboardState,
    MouseButton,
    MouseState,
)


class RaylibWindow:
    def __init__(self, title: str) -> None:
        self.title = title

    def open(self, width: int, height: int) -> None:
        raylib.init_window(width, height, self.title)

    def close(self) -> None:
        raylib.close_window()

    def is_open(self) -> bool:
        return not raylib.window_should_close()


class RaylibRenderer:
    def __init__(self) -> None:
        self._loaded_textures: dict[str, raylib.Texture] = {}

    def initialize(self) -> None:
        pass

    def teardown(self) -> None:
        for texture in self._loaded_textures.values():
            raylib.unload_texture(texture)

    def begin_frame(self) -> None:
        raylib.begin_drawing()
        raylib.clear_background(raylib.BLACK)

    def end_frame(self) -> None:
        raylib.draw_fps(10, 10)
        raylib.end_drawing()

    def is_texture_loaded(self, texture_path: str) -> bool:
        return texture_path in self._loaded_textures

    def load_texture(self, texture_path: str) -> raylib.Texture:
        if not self.is_texture_loaded(texture_path):
            self._loaded_textures[texture_path] = raylib.load_texture(texture_path)
        return self._loaded_textures[texture_path]

    def draw_sprite(self, texture_path: str, x: int, y: int) -> None:
        texture: raylib.Texture = self.load_texture(texture_path)
        raylib.draw_texture(texture, x, y, raylib.WHITE)

    def draw_text(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int = 12,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
    ) -> None:
        raylib.draw_text(text, x, y, font_size, color)


class RaylibInputSource:
    def _set_controller_state(self, state: ControllerState) -> None:
        pass

    def _set_keyboard_state(self, state: KeyboardState) -> None:
        state.keys[KeyboardKey.W] = raylib.is_key_down(raylib.KeyboardKey.KEY_W)

    def _set_mouse_state(self, state: MouseState) -> None:
        state.buttons[MouseButton.LEFT] = raylib.is_mouse_button_down(
            raylib.MouseButton.MOUSE_BUTTON_LEFT
        )
        state.buttons[MouseButton.MIDDLE] = raylib.is_mouse_button_down(
            raylib.MouseButton.MOUSE_BUTTON_MIDDLE
        )
        state.buttons[MouseButton.RIGHT] = raylib.is_mouse_button_down(
            raylib.MouseButton.MOUSE_BUTTON_RIGHT
        )
        state.buttons[MouseButton.FORWARD] = raylib.is_mouse_button_down(
            raylib.MouseButton.MOUSE_BUTTON_FORWARD
        )
        state.buttons[MouseButton.BACK] = raylib.is_mouse_button_down(
            raylib.MouseButton.MOUSE_BUTTON_BACK
        )

    def set_input_state(self, state: InputState) -> None:
        self._set_controller_state(state.controller_state)
        self._set_keyboard_state(state.keyboard_state)
        self._set_mouse_state(state.mouse_state)
