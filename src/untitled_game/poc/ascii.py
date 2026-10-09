import msvcrt
import sys

from .game import Game
from .map import Map
from .player import Player
from .tile import Tile


class AsciiRenderer:
    def __init__(self) -> None:
        self._stream = sys.stdout
        self._character_map: dict[Tile, str] = {
            Tile.BARRIER: "X",
            Tile.DIRT: "$",
            Tile.GRASS: ".",
            Tile.ROAD: "O",
        }

    def render(self, game: Game) -> None:
        self._clear()
        self._draw_map(game.map)
        self._draw_player(game.player)
        self._draw_ui(game)

    def _draw_map(self, map: Map) -> None:
        for i, tile in enumerate(map.tiles):
            row: int = i // map.columns
            column: int = i % map.columns
            character = self._character_map[tile]
            self._write_at(row, column, character)

    def _draw_player(self, player: Player) -> None:
        player_row: int = int(player.y)
        player_column: int = int(player.x)
        self._write_at(player_row, player_column, "P")

    def _write_at(self, row: int, col: int, text: str) -> None:
        # Move cursor to row, column (1-based)
        ROW_OFFSET: int = 1
        COLUMN_OFFSET: int = 1
        self._stream.write(f"\033[{row + ROW_OFFSET};{col + COLUMN_OFFSET}H")
        self._stream.write(text)
        self._stream.flush()

    def _write_field(self, row: int, col: int, text: str, width: int) -> None:
        self._write_at(row, col, f"{text:<{width}}"[:width])

    def _clear(self) -> None:
        self._stream.write("\033[2J\033[H")
        self._stream.flush()

    def _draw_ui(self, game: Game) -> None:
        self._write_field(
            game.map.rows + 1, 0, f"Map(rows={game.map.rows}, columns={game.map.columns})", 50
        )
        self._write_field(game.map.rows + 2, 0, str(game.player), 50)
        self._write_field(
            game.map.rows + 3, 0, f"Input Vector: {game.player_controller.get_input_vector()!s}", 50
        )


class AsciiWindow:
    def open(self, width: int, height: int, title: str) -> None:
        pass

    def is_open(self) -> bool:
        return True

    def close(self) -> None:
        pass


class TerminalController:
    def get_input_vector(self) -> tuple[float, float]:
        NO_INPUT: tuple[float, float] = (0.0, 0.0)

        if not msvcrt.kbhit():  # key pressed?
            return NO_INPUT

        key = msvcrt.getch()
        if key not in (b"\x00", b"\xe0"):  # windows: arrow keys are 2 bytes
            return NO_INPUT

        key = msvcrt.getch()  # reads second byte

        return {
            b"H": (0, -1),  # up
            b"P": (0, 1),  # down
            b"K": (-1, 0),  # left
            b"M": (1, 0),  # right
        }.get(key, NO_INPUT)
