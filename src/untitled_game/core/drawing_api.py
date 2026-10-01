from typing import Protocol


class DrawingAPI(Protocol):
    def draw_circle(
        self, x: int, y: int, radius: float, color: tuple[int, int, int, int]
    ) -> None: ...
