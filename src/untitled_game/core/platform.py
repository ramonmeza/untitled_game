from typing import Protocol

from .clock import Clock
from .drawing_api import DrawingAPI
from .renderer import Renderer
from .window import Window


class Platform(Protocol):
    @property
    def clock(self) -> Clock: ...

    @property
    def drawing_api(self) -> DrawingAPI: ...

    @property
    def renderer(self) -> Renderer: ...

    @property
    def window(self) -> Window: ...
