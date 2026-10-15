from dataclasses import dataclass

from .engine import Engine
from .window import Window


@dataclass
class ApplicationConfig:
    window_width: int = 800
    window_height: int = 800


class Application:
    def __init__(self, window: Window) -> None:
        self._engine: Engine = Engine()
        self._config: ApplicationConfig = ApplicationConfig()
        self._window: Window = window

    def run(self) -> None:
        self.initialize()
        self.loop()
        self.teardown()

    def initialize(self) -> None:
        self._window.open(self._config.window_width, self._config.window_height)
        self._engine.initialize()

    def loop(self) -> None:
        while self._window.is_open():
            self._engine.update()

    def teardown(self) -> None:
        self._engine.teardown()
        self._window.close()
