from random import choice

from .input_controller import InputController
from .map import Map
from .player import Player
from .raylib_controller import RaylibController
from .tile import Tile


def pick_random_tile() -> Tile:
    return choice(list(Tile))


def generate_map(rows: int, columns: int) -> Map:
    tiles: list[Tile] = [pick_random_tile() for _ in range(rows * columns)]
    map: Map = Map(tiles, rows, columns)
    return map


class Game:
    TILE_MAP_ROWS: int = 10
    TILE_MAP_COLUMNS: int = 20

    def __init__(self) -> None:
        self.map: Map = generate_map(Game.TILE_MAP_ROWS, Game.TILE_MAP_COLUMNS)
        self.player: Player = Player()
        self.player_controller: InputController = RaylibController()

    def move_player(self, input_vector: tuple[float, float]) -> None:
        self.player.x = self.player.x + max(-1, min(input_vector[0], 1)) * 0.001
        self.player.y = self.player.y + max(-1, min(input_vector[1], 1)) * 0.001

    def update(self) -> None:
        input_vector: tuple[float, float] = self.player_controller.get_input_vector()
        self.move_player(input_vector)
