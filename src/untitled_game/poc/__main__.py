from dataclasses import dataclass, field
from time import perf_counter, sleep

import pyray as raylib


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


class GameInput:
    def __init__(self) -> None:
        self._accelerator: float = 0.0
        self._brake: float = 0.0
        self._ebrake: float = 0.0
        self._steering: float = 0.0

    def __str__(self) -> str:
        attrs: list[str] = [
            f"{attr.removeprefix('_')}={getattr(self, attr.removeprefix('_'))!s}"
            for attr in vars(self)
        ]
        return f"<GameInput {' '.join(attrs)}>"

    @property
    def accelerator(self) -> float:
        return self._accelerator

    @accelerator.setter
    def accelerator(self, value: float) -> None:
        self._accelerator = clamp(value, 0, 1)

    @property
    def brake(self) -> float:
        return self._brake

    @brake.setter
    def brake(self, value: float) -> None:
        self._brake = clamp(value, 0, 1)

    @property
    def ebrake(self) -> float:
        return clamp(self._ebrake, 0, 1)

    @ebrake.setter
    def ebrake(self, value: float) -> None:
        self._ebrake = clamp(value, 0, 1)

    @property
    def steering(self) -> float:
        return self._steering

    @steering.setter
    def steering(self, value: float) -> None:
        self._steering = clamp(value, -1, 1)


@dataclass
class GameState:
    """Mutable values for the game."""

    player_input: GameInput = field(default_factory=GameInput)


class Game:
    def __init__(self) -> None:
        self.player_controller: PlayerController = PlayerController()
        self.game_state: GameState = GameState()

    def update(self, delta_time: float) -> None:
        game_input: GameInput = self.player_controller.poll_input()
        self.game_state.player_input = game_input


class Renderer:
    def draw_game(self, game: Game) -> None:
        pass

    def _draw_ui_bar(
        self,
        text: str,
        x: int,
        y: int,
        width: int = 12,
        height: int = 100,
        value: float = 0,
        font_color: raylib.Color = raylib.BLACK,
        font_size: int = 12,
        color: raylib.Color = raylib.GREEN,
    ) -> None:
        raylib.draw_rectangle_lines(x, y, width, height, color)
        raylib.draw_rectangle(
            x,
            y,
            int(width * value),
            height,
            color,
        )
        raylib.draw_text(text, x + 2, y, font_size, font_color)

    def draw_ui(self, game: Game) -> None:
        x: int = 10
        y: int = 40
        bar_height: int = 12
        bar_width: int = 100
        font_size: int = 12
        vspacing: int = 2
        vpadding: int = 4
        hpadding: int = 6
        num_bars: int = 4
        bg_x = x - hpadding
        bg_y = y - vpadding
        bg_width: int = hpadding + bar_width + hpadding
        bg_height: int = (
            vpadding + (bar_height * num_bars) + (num_bars * vspacing) - vspacing + vpadding
        )

        raylib.draw_rectangle(bg_x, bg_y, bg_width, bg_height, raylib.DARKGRAY)

        self._draw_ui_bar(
            "Accelerator",
            x,
            y,
            bar_width,
            bar_height,
            game.game_state.player_input.accelerator,
            raylib.WHITE,
            font_size,
            raylib.GREEN,
        )
        y += bar_height + vspacing

        self._draw_ui_bar(
            "Brake",
            x,
            y,
            bar_width,
            bar_height,
            game.game_state.player_input.brake,
            raylib.WHITE,
            font_size,
            raylib.RED,
        )
        y += bar_height + vspacing

        self._draw_ui_bar(
            "E-Brake",
            x,
            y,
            bar_width,
            bar_height,
            game.game_state.player_input.ebrake,
            raylib.WHITE,
            font_size,
            raylib.PURPLE,
        )
        y += bar_height + vspacing

        half_bar_width: int = int(bar_width / 2)
        raylib.draw_rectangle_lines(x, y, bar_width, bar_height, raylib.BLUE)
        val = int(half_bar_width * game.game_state.player_input.steering)
        print(val)
        if val > 0:
            raylib.draw_rectangle(
                x + half_bar_width,
                y,
                val,
                bar_height,
                raylib.BLUE,
            )
        else:
            abs_val: float = abs(val)
            raylib.draw_rectangle(x + half_bar_width - abs_val, y, abs_val, bar_height, raylib.BLUE)
        raylib.draw_text("Steering", x, y, font_size, raylib.WHITE)

    def render(self, game: Game) -> None:
        # camera data will eventually come from Game
        camera = raylib.Camera2D()

        raylib.begin_drawing()
        raylib.clear_background(raylib.BLACK)
        raylib.begin_mode_2d(camera)
        self.draw_game(game)
        raylib.end_mode_2d()
        self.draw_ui(game)
        raylib.draw_fps(10, 10)
        raylib.end_drawing()


class PlayerController:
    def poll_input(self) -> GameInput:
        game_input: GameInput = GameInput()

        game_input.accelerator = float(raylib.is_key_down(raylib.KeyboardKey.KEY_W))
        game_input.brake = float(raylib.is_key_down(raylib.KeyboardKey.KEY_S))
        game_input.ebrake = float(raylib.is_key_down(raylib.KeyboardKey.KEY_SPACE))

        game_input.steering = 0.0  # recenter, wouldnt be necessary with analog stick
        steer_left: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_A) else 0
        steer_right: float = 1.0 if raylib.is_key_down(raylib.KeyboardKey.KEY_D) else 0
        steering: float = steer_right - steer_left
        game_input.steering = steering

        return game_input


class Timer:
    def __init__(self, rate: float = 0.0) -> None:
        rate = max(0, rate)
        self.frame_interval: float = rate
        self.prev_time: float = perf_counter()
        self.next_frame_time: float = self.prev_time + rate

    def tick(self) -> float:
        now: float = perf_counter()
        remaining: float = self.next_frame_time - now
        if remaining > 0.0:
            sleep(remaining)

        now = perf_counter()
        delta_time: float = now - self.prev_time
        self.prev_time = now
        self.next_frame_time += self.frame_interval

        if self.next_frame_time < now:
            self.next_frame_time = now + self.frame_interval

        return delta_time


def main() -> None:
    FPS_LOCK: int = 60
    raylib.init_window(800, 600, "Proof of Concept")
    renderer: Renderer = Renderer()
    frame_timer: Timer = Timer(1 / FPS_LOCK)
    game: Game = Game()

    while not raylib.window_should_close():
        delta_time: float = frame_timer.tick()
        game.update(delta_time)
        renderer.render(game)
        print(str(game.game_state.player_input))

    raylib.close_window()


main()
