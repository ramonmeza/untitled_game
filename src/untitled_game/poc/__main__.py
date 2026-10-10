from dataclasses import dataclass
from time import perf_counter


@dataclass
class GameInput:
    """Normalized [0, 1] inputs for the game."""

    accelerator: float = 0.0
    brake: float = 0.0
    ebrake: float = 0.0


@dataclass
class GameState:
    """Mutable values for the game."""


class Game:
    def __init__(self) -> None:
        self.game_state: GameState = GameState()

    def update(self, game_input: GameInput, delta_time: float) -> None:
        pass


class Renderer:
    def render(self, game: Game) -> None:
        pass


class PlayerController:
    def poll_input(self) -> GameInput:
        return GameInput()


def main() -> None:
    renderer: Renderer = Renderer()
    prev_time: float = perf_counter()
    delta_time: float = 0.0
    is_running: bool = True
    game: Game = Game()

    player_controller: PlayerController = PlayerController()

    while is_running:
        now_time: float = perf_counter()
        delta_time = now_time - prev_time
        prev_time = now_time

        game_input: GameInput = player_controller.poll_input()
        game.update(game_input, delta_time)
        renderer.render(game)


main()
