from .core.game import Game
from .core.platform import Platform
from .settings import (
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


class Application:
    def __init__(self, platform: Platform, game: Game) -> None:
        self._platform: Platform = platform
        self._game: Game = game

    def _initialize(self) -> None:
        self._platform.window.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    def _shutdown(self) -> None:
        self._platform.window.close_window()

    def _update(self) -> None:
        delta_time: float = self._platform.clock.get_delta_time()
        self._game.update(delta_time)

    def _render(self) -> None:
        self._platform.renderer.begin_frame()
        self._platform.renderer.clear_frame()
        self._game.draw(self._platform.drawing_api)
        self._platform.renderer.end_frame()

    def run(self) -> None:
        self._initialize()
        try:
            while self._platform.window.is_open():
                self._update()
                self._render()
        finally:
            self._shutdown()
