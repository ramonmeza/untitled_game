from typing import Protocol

from .game import Game


class Renderer(Protocol):
    def render(self, game: Game) -> None: ...
