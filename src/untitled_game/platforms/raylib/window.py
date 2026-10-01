import pyray as raylib


class RaylibWindow:
    def open_window(self, width: int, height: int, title: str) -> None:
        raylib.init_window(width, height, title)

    def is_open(self) -> bool:
        return not raylib.window_should_close()

    def close_window(self) -> None:
        raylib.close_window()
