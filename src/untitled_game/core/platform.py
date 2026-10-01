from typing import Protocol

from .clock import Clock
from .renderer import Renderer
from .window import Window


class Platform(Protocol):
    @property
    def clock(self) -> Clock: ...

    @property
    def renderer(self) -> Renderer: ...

    @property
    def window(self) -> Window: ...
