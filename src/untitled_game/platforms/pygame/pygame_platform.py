import pygame

from .pygame_clock import PygameClock
from .pygame_drawing_api import PygameDrawingAPI
from .pygame_renderer import PygameRenderer
from .pygame_window import PygameWindow


class PygamePlatform:
    def __init__(self) -> None:
        pygame.init()
        self.clock: PygameClock = PygameClock()
        self.drawing_api: PygameDrawingAPI = PygameDrawingAPI()
        self.renderer: PygameRenderer = PygameRenderer()
        self.window: PygameWindow = PygameWindow()
