import pyray as raylib


class RaylibDrawingAPI:
    def draw_circle(self, x: int, y: int, radius: float, color: tuple[int, int, int, int]) -> None:
        raylib.draw_circle(x, y, radius, color)  # pyright: ignore[reportUnknownMemberType]
