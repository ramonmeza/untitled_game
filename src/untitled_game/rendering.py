# pyright: reportUnknownMemberType=false
import pyray as raylib

from .actions import ActionID
from .camera import Camera
from .components import BoxComponent, PositionComponent
from .ecs import ECS
from .game import Game
from .ui import UIStyle


class Renderer:
    """
    Rendering the UI and GameState. Currently tightly coupled to raylib. We can
    think of an abstraction layer once we need it.
    """

    def __init__(self) -> None:
        self.ui_style: UIStyle = UIStyle()
        self.render_system: RenderSystem = RenderSystem()
        self.camera: raylib.Camera2D = raylib.Camera2D(
            (raylib.get_render_width() / 2, raylib.get_render_height() / 2),
            raylib.Vector2(0, 0),
            0.0,
            1.0,
        )

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

    def draw_background_grid(self) -> None:
        """
        Could use a full screen shader that uses camera position to generate the grid, but thats a
        bigger task than just manually calling draw a set number of times. But this is very
        inefficient, since we do it every frame.
        """
        grid_size: int = 32
        grid_rows: int = 50
        grid_cols: int = 20
        for y in range(grid_rows):
            for x in range(grid_cols):
                grid_color = raylib.LIGHTGRAY if (x + y) % 2 == 0 else raylib.DARKGRAY
                raylib.draw_rectangle(
                    x * grid_size, y * grid_size, grid_size, grid_size, grid_color
                )

    def draw_game(self, game: Game) -> None:
        self.draw_background_grid()
        self.render_system.update(game.ecs)

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

        value: float = float(
            game.get_action_value(game.get_player_entity_id(), ActionID.ACCELERATE, 0.0)
        )
        self._draw_ui_progress_bar(
            "Accelerator",
            x,
            y,
            value=value,
            color=raylib.GREEN,
        )
        y += self.ui_style.bar_height + self.ui_style.vspacing

        value = float(game.get_action_value(game.get_player_entity_id(), ActionID.BRAKE, 0.0))
        self._draw_ui_progress_bar("Brake", x, y, value=value, color=raylib.RED)
        y += self.ui_style.bar_height + self.ui_style.vspacing

        value = float(game.get_action_value(game.get_player_entity_id(), ActionID.EBRAKE, 0.0))
        self._draw_ui_progress_bar("E-Brake", x, y, value=value, color=raylib.PURPLE)
        y += self.ui_style.bar_height + self.ui_style.vspacing

        # centered progress bar
        half_bar_width: int = int(self.ui_style.bar_width / 2)
        raylib.draw_rectangle_lines(
            x, y, self.ui_style.bar_width, self.ui_style.bar_height, raylib.BLUE
        )
        value = float(game.get_action_value(game.get_player_entity_id(), ActionID.STEERING, 0.0))
        progress_bar_fill_width: int = int(half_bar_width * value)
        if progress_bar_fill_width > 0:
            raylib.draw_rectangle(
                x + half_bar_width,
                y,
                progress_bar_fill_width,
                self.ui_style.bar_height,
                raylib.BLUE,
            )
        else:
            abs_progress_bar_fill_width: float = abs(progress_bar_fill_width)
            raylib.draw_rectangle(
                x + half_bar_width - abs_progress_bar_fill_width,
                y,
                abs_progress_bar_fill_width,
                self.ui_style.bar_height,
                raylib.BLUE,
            )
        raylib.draw_text("Steering", x, y, self.ui_style.font_size, raylib.WHITE)
        y += self.ui_style.bar_height + self.ui_style.vspacing

        value = float(game.get_action_value(game.get_player_entity_id(), ActionID.ACTIVATE, False))
        self._draw_ui_progress_bar(
            "Activate",
            x,
            y,
            value=value,
            color=raylib.ORANGE,
        )

    def update_camera(self, camera: Camera) -> None:
        self.camera.target.x = camera.position.x
        self.camera.target.y = camera.position.y
        self.camera.zoom = camera.zoom

    def render(self, game: Game) -> None:
        self.update_camera(game.main_camera)
        raylib.begin_drawing()
        raylib.clear_background(raylib.BLACK)
        raylib.begin_mode_2d(self.camera)
        self.draw_game(game)
        raylib.end_mode_2d()
        self.draw_ui(game)
        raylib.draw_fps(10, 10)
        raylib.end_drawing()


class RenderSystem:
    def update(self, ecs: ECS) -> None:
        entities_with_renderables: list[int] = ecs.get_all_entities_with_components(
            BoxComponent, PositionComponent
        )
        for entity_id in entities_with_renderables:
            pos_comp: PositionComponent = ecs.get_components_of_type(entity_id, PositionComponent)[
                0
            ]
            box_comp: BoxComponent = ecs.get_components_of_type(entity_id, BoxComponent)[0]

            raylib.draw_rectangle(
                int(pos_comp.x), int(pos_comp.y), box_comp.width, box_comp.height, raylib.PINK
            )
