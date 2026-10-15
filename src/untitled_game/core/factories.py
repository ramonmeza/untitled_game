from .input import InputSource
from .renderer import Renderer
from .window import Window


def create_input_source() -> InputSource:
    from .integrations.raylib import RaylibInputSource

    return RaylibInputSource()


def create_renderer() -> Renderer:
    from .integrations.raylib import RaylibRenderer

    return RaylibRenderer()


def create_window(title: str) -> Window:
    from .integrations.raylib import RaylibWindow

    return RaylibWindow(title)
