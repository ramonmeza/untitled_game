import pyray as raylib


class RaylibController:
    def get_input_vector(self) -> tuple[float, float]:
        x = y = 0
        x -= int(raylib.is_key_down(raylib.KeyboardKey.KEY_A))
        x += int(raylib.is_key_down(raylib.KeyboardKey.KEY_D))
        y -= int(raylib.is_key_down(raylib.KeyboardKey.KEY_W))
        y += int(raylib.is_key_down(raylib.KeyboardKey.KEY_S))
        return (x, y)
