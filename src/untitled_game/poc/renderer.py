from typing import Protocol

from .game import Game


class Renderer(Protocol):
    def clear(self) -> None: ...
    def draw(self, game: Game) -> None: ...
