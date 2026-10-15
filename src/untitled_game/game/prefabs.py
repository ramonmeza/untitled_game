from ..core.components import SpriteComponent, TransformComponent
from ..core.world.world import World


def create_player_entity(world: World) -> None:
    world.create_entity(
        TransformComponent(),
        SpriteComponent(r"assets\textures\colorful_pyramid.png"),
    )


def create_empty_world() -> World:
    world: World = World()
    return world


def create_dev_world() -> World:
    world: World = World()
    create_player_entity(world)
    return world
