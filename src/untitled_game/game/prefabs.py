from pathlib import Path

from ..core import Vector2
from ..core.components import SpriteComponent, TransformComponent
from ..core.world.world import World


def create_player_entity(world: World) -> None:
    world.create_entity(
        TransformComponent(Vector2(300, 300), 45.0),
        SpriteComponent(Path("assets") / "textures" / "colorful_pyramid.png"),
    )


def create_empty_world() -> World:
    world: World = World()
    return world


def create_dev_world() -> World:  # pragma: no cover
    world: World = World()
    create_player_entity(world)
    return world
