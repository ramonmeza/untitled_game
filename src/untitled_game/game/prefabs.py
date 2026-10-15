from ..core import Vector2
from ..core.components import SpriteComponent, TransformComponent
from ..core.world.world import World


def create_player_entity(world: World) -> None:
    world.create_entity(
        TransformComponent(position=Vector2(0, 0), rotation=0, scale=Vector2(0, 0)),
        SpriteComponent(r"assets\textures\colorful_pyramid.png"),
    )


def load_world() -> World:
    world: World = World()
    create_player_entity(world)
    return world
