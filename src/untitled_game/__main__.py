"""
Design Philosophy: A game takes inputs, updates its internal state through systems, and produces a
view for the renderer to visualize.

`main()` is at the bottom. It manages the application lifecycle.

Controls (DEBUG PHASE):
W - Accelerator
S - Brake
A - Steer Left
D - Steer Right
SPACE - E-Brake
E - Activate

Requirements:
- Game has a GameState
- GameState is modified by GameInputs
- Game has Controllers which produce GameInputs
- Game manages order to process GameInput
- Game modifies GameState through Systems
- Systems modify GameState by a set of rules (gameplay design)
- Game manages the order the Systems process the GameState
- Game will produce a UIView.
- Renderer manages rendering a frame from a Game.
- Renderer will be able to render a GameState
- Renderer will be able to render UI from a UIView

Entity Component System:
- Entities have IDs.
- Components contain data.
- Systems read and react to Components' data.
- There are mappings between entities and their component data.

- Game will have a single Camera object
"""

import pyray as raylib

from .game import Game
from .rendering import Renderer


def main() -> None:
    GAME_TICK_RATE: float = 1 / 60
    """
    Game updates at this rate interval no matter what.
    Rendering occurs as fast as possible.
    So, FPS could be high, but depending on `GAME_TICK_RATE`, the game state will only change so fast.
    Rendering *could* handle interpolation of the frame data, which would be so cool. I think you'd 
    need a frame buffer and alway have a 1 frame latency.
    """

    raylib.init_window(800, 600, "Untitled Game")
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
