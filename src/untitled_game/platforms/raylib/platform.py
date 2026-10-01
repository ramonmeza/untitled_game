from .clock import RaylibClock
from .renderer import RaylibRenderer
from .window import RaylibWindow


class RaylibPlatform:
    def __init__(self) -> None:
        self.clock: RaylibClock = RaylibClock()
        self.renderer: RaylibRenderer = RaylibRenderer()
        self.window: RaylibWindow = RaylibWindow()
