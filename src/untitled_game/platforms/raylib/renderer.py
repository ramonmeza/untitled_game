import pyray as raylib


class RaylibRenderer:
    def begin_frame(self) -> None:
        raylib.begin_drawing()

    def clear_frame(self) -> None:
        raylib.clear_background(raylib.BLACK)  # pyright: ignore[reportUnknownMemberType]

    def end_frame(self) -> None:
        raylib.end_drawing()
