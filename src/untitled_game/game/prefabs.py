from importlib.resources import files
from importlib.resources.abc import Traversable

from ..core import Vector2
from ..core.components import SpriteComponent, TransformComponent
from ..core.world.world import World

ASSET_DIR: Traversable = files("untitled_game") / "assets"


def create_player_entity(world: World) -> None:
    sprite_path: str = str(ASSET_DIR / "textures" / "colorful_pyramid.png")
    world.create_entity(
        TransformComponent(Vector2(300, 200)),
        SpriteComponent(sprite_path),
    )


def create_empty_world() -> World:
    world: World = World()
    return world


def create_dev_world() -> World:
    world: World = World()
    create_player_entity(world)
    return world
