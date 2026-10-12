import pyray as raylib

from .game import Game
from .rendering import Renderer

GAME_TITLE: str = "Untitled Game"
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
GAME_TICK_RATE: float = 1 / 60


def main() -> None:
    raylib.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
    renderer: Renderer = Renderer()
    game: Game = Game()
    game.load()

    time_accumulator: float = 0.0
    while not raylib.window_should_close():
        delta_time: float = raylib.get_frame_time()
        time_accumulator += delta_time
        while time_accumulator >= GAME_TICK_RATE:
            game.tick(GAME_TICK_RATE)
            time_accumulator -= GAME_TICK_RATE
        renderer.render(game)

    raylib.close_window()


main()
