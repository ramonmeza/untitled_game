from ..core.drawing_api import DrawingAPI
from .player import Player


class UntitledGame:
    def __init__(self) -> None:
        self._player = Player()

    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, drawer: DrawingAPI) -> None:
        self.draw_player(drawer)

    def draw_player(self, drawer: DrawingAPI) -> None:
        drawer.draw_circle(int(self._player.x), int(self._player.y), 10.0, (255, 0, 0, 255))
