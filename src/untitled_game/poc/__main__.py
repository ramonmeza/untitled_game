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
"""

from dataclasses import dataclass, field
from time import perf_counter, sleep
from uuid import uuid4

import pyray as raylib


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


class GameInput:
    """Represents inputs used to modify the state of the game."""

    def __init__(self) -> None:
        self._accelerator: float = 0.0
        self._brake: float = 0.0
        self._ebrake: float = 0.0
        self._steering: float = 0.0
        self._activate: bool = False

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

    @property
    def activate(self) -> bool:
        return self._activate

    @activate.setter
    def activate(self, value: bool) -> None:
        self._activate = value


@dataclass
class GameState:
    """Mutable values for the game."""

    player_input: GameInput = field(default_factory=GameInput)


class Controller:
    """
    Used to connect hardware to the game. Would need an abstraction if we dont want to call raylib directly.
    Will have to think about how to abstract input, but this gives us a hook we could eventually refactor.
    """

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

        game_input.activate = raylib.is_key_down(raylib.KeyboardKey.KEY_E)

        return game_input


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@dataclass
class BoxComponent:
    width: int
    height: int


class RenderSystem:
    def update(
        self,
        position_components: dict[int, PositionComponent],
        box_components: dict[int, BoxComponent],
    ) -> None:
        for entity_id, box_comp in box_components.items():
            pos_comp = position_components.get(entity_id, None)
            if pos_comp is None:
                continue

            raylib.draw_rectangle(
                int(pos_comp.x), int(pos_comp.y), box_comp.width, box_comp.height, raylib.PINK
            )


class Game:
    """Manages the GameState, which is modified by Controllers."""

    def __init__(self) -> None:
        self.player_controller: Controller = Controller()
        self.game_state: GameState = GameState()
        self.entities: list[int] = []
        self.position_components: dict[int, PositionComponent] = {}
        self.box_components: dict[int, BoxComponent] = {}
        self.render_system: RenderSystem = RenderSystem()

    def load(self) -> None:
        self._create_player()

    def generate_entity_id(self) -> int:
        return uuid4().int

    def _create_player(self) -> None:
        entity_id: int = self.create_entity()
        self.position_components[entity_id] = PositionComponent(100, 200)
        self.box_components[entity_id] = BoxComponent(200, 100)

    def create_entity(self) -> int:
        entity_id: int = self.generate_entity_id()
        self.entities.append(entity_id)
        return entity_id

    def get_input(self) -> None:
        game_input: GameInput = self.player_controller.poll_input()
        self.game_state.player_input = game_input

    def update_systems(self) -> None:
        self.render_system.update(self.position_components, self.box_components)

    def update(self, delta_time: float) -> None:
        self.get_input()
        self.update_systems()


@dataclass
class UIStyle:
    font_color: raylib.Color = field(default=raylib.WHITE)
    bar_height: int = 12
    bar_width: int = 100
    font_size: int = 12
    vspacing: int = 2
    vpadding: int = 4
    hpadding: int = 6


class Renderer:
    """
    Rendering the UI and GameState. Currently tightly coupled to raylib. We can
    think of an abstraction layer once we need it.
    """

    def __init__(self) -> None:
        self.ui_style: UIStyle = UIStyle()

    def draw_game(self, game: Game) -> None:
        pass

    def _draw_ui_progress_bar(
        self,
        text: str,
        x: int,
        y: int,
        width: int = 100,
        height: int = 12,
        value: float = 0,
        color: raylib.Color = raylib.BLANK,
    ) -> None:
        raylib.draw_rectangle_lines(x, y, width, height, color)
        raylib.draw_rectangle(x, y, int(width * value), height, color)
        raylib.draw_text(text, x + 2, y, self.ui_style.font_size, self.ui_style.font_color)

    def draw_ui(self, game: Game) -> None:
        x: int = 10
        y: int = 40
        num_bars: int = 5
        bg_x = x - self.ui_style.hpadding
        bg_y = y - self.ui_style.vpadding
        bg_width: int = self.ui_style.hpadding + self.ui_style.bar_width + self.ui_style.hpadding
        bg_height: int = (
            self.ui_style.vpadding
            + (self.ui_style.bar_height * num_bars)
            + (num_bars * self.ui_style.vspacing)
            - self.ui_style.vspacing
            + self.ui_style.vpadding
        )

        raylib.draw_rectangle(bg_x, bg_y, bg_width, bg_height, raylib.DARKGRAY)

        self._draw_ui_progress_bar(
            "Accelerator", x, y, value=game.game_state.player_input.accelerator, color=raylib.GREEN
        )
        y += self.ui_style.bar_height + self.ui_style.vspacing

        self._draw_ui_progress_bar(
            "Brake", x, y, value=game.game_state.player_input.brake, color=raylib.RED
        )
        y += self.ui_style.bar_height + self.ui_style.vspacing

        self._draw_ui_progress_bar(
            "E-Brake", x, y, value=game.game_state.player_input.ebrake, color=raylib.PURPLE
        )
        y += self.ui_style.bar_height + self.ui_style.vspacing

        # centered progress bar
        half_bar_width: int = int(self.ui_style.bar_width / 2)
        raylib.draw_rectangle_lines(
            x, y, self.ui_style.bar_width, self.ui_style.bar_height, raylib.BLUE
        )
        val: int = int(half_bar_width * game.game_state.player_input.steering)
        if val > 0:
            raylib.draw_rectangle(
                x + half_bar_width,
                y,
                val,
                self.ui_style.bar_height,
                raylib.BLUE,
            )
        else:
            abs_val: float = abs(val)
            raylib.draw_rectangle(
                x + half_bar_width - abs_val, y, abs_val, self.ui_style.bar_height, raylib.BLUE
            )
        raylib.draw_text("Steering", x, y, self.ui_style.font_size, raylib.WHITE)
        y += self.ui_style.bar_height + self.ui_style.vspacing

        self._draw_ui_progress_bar(
            "Activate",
            x,
            y,
            value=float(game.game_state.player_input.activate),
            color=raylib.ORANGE,
        )

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


class FrameTimer:
    def __init__(self, frame_interval: float = 0.0) -> None:
        """
        :rate:
        :type rate: float
        """
        self.frame_interval: float = max(0, frame_interval)
        self.prev_time: float = perf_counter()
        self.next_frame_time: float = self.prev_time + self.frame_interval

    def tick(self) -> float:
        """
        :rtype: float
        :return: time since `tick()` was last called."""
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
    frame_timer: FrameTimer = FrameTimer(1 / FPS_LOCK)
    game: Game = Game()
    game.load()
    while not raylib.window_should_close():
        delta_time: float = frame_timer.tick()
        game.update(delta_time)
        renderer.render(game)

    raylib.close_window()


main()
