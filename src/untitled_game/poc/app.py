from .game import Game
from .renderer import Renderer
from .window import Window


class App:
    def __init__(self, window: Window, renderer: Renderer, game: Game) -> None:
        self._window: Window = window
        self._game: Game = game
        self._renderer: Renderer = renderer

    def run(self) -> None:
        self._window.open(800, 600, "Proof of Concept")
        try:
            while self._window.is_open():
                self._game.update()
                self._renderer.render(self._game)
        finally:
            self._window.close()
