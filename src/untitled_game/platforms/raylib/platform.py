from .clock import RaylibClock
from .drawing_api import RaylibDrawingAPI
from .renderer import RaylibRenderer
from .window import RaylibWindow


class RaylibPlatform:
    def __init__(self) -> None:
        self.clock: RaylibClock = RaylibClock()
        self.drawing_api: RaylibDrawingAPI = RaylibDrawingAPI()
        self.renderer: RaylibRenderer = RaylibRenderer()
        self.window: RaylibWindow = RaylibWindow()
