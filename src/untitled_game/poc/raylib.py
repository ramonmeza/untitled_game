import pyray as raylib

from .game import Game
from .map import Map
from .player import Player
from .tile import Tile


class RaylibRenderer:
    def __init__(self) -> None:
        self._tile_map_grid_size: int = 32
        self._tile_map: dict[Tile, raylib.Color] = {
            Tile.BARRIER: raylib.BLUE,
            Tile.DIRT: raylib.BROWN,
            Tile.GRASS: raylib.GREEN,
            Tile.ROAD: raylib.GRAY,
        }

    def render(self, game: Game) -> None:
        raylib.begin_drawing()
        raylib.clear_background(raylib.BLACK)
        self._draw_map(game.map)
        self._draw_player(game.player)
        self._draw_ui(game)
        raylib.end_drawing()

    def _draw_player(self, player: Player) -> None:
        x: int = int(player.x * self._tile_map_grid_size)
        y: int = int(player.y * self._tile_map_grid_size)
        radius: float = self._tile_map_grid_size / 2
        raylib.draw_circle(x, y, radius, raylib.PURPLE)

    def _draw_tile(self, row: int, column: int, tile: Tile) -> None:
        x: int = column * self._tile_map_grid_size
        y: int = row * self._tile_map_grid_size
        width = height = self._tile_map_grid_size
        tile_color = self._tile_map.get(tile, raylib.BLACK)
        raylib.draw_rectangle(x, y, width, height, tile_color)

    def _draw_map(self, map: Map) -> None:
        for i, tile in enumerate(map.tiles):
            row: int = i // map.columns
            column: int = i % map.columns
            self._draw_tile(row, column, tile)

    def _draw_ui(self, game: Game) -> None:
        font_size: int = 20
        x = 10
        y = game.map.rows * self._tile_map_grid_size
        raylib.draw_text(
            f"Map(rows={game.map.rows}, columns={game.map.columns})", x, y, font_size, raylib.PINK
        )
        raylib.draw_text(str(game.player), x, y + (font_size * 2), font_size, raylib.PINK)
        raylib.draw_text(
            f"Input Vector: {game.player_controller.get_input_vector()!s}",
            x,
            y + (font_size * 4),
            font_size,
            raylib.PINK,
        )


class RaylibWindow:
    def open(self, width: int, height: int, title: str) -> None:
        raylib.init_window(width, height, title)

    def is_open(self) -> bool:
        return not raylib.window_should_close()

    def close(self) -> None:
        raylib.close_window()


class RaylibController:
    def __init__(self) -> None:
        pass

    def get_input_vector(self) -> tuple[float, float]:
        x = y = 0
        x -= int(raylib.is_key_down(raylib.KeyboardKey.KEY_A))
        x += int(raylib.is_key_down(raylib.KeyboardKey.KEY_D))
        y -= int(raylib.is_key_down(raylib.KeyboardKey.KEY_W))
        y += int(raylib.is_key_down(raylib.KeyboardKey.KEY_S))
        return (x, y)
