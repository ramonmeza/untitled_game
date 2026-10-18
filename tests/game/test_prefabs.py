from untitled_game.core.world.world import World
from untitled_game.game import prefabs


def test_create_player_entity_creates_new_entity() -> None:
    world: World = prefabs.create_empty_world()

    entities_before_creation: list[int] = world.get_all_entities()
    prefabs.create_player_entity(world)
    entities_after_creation: list[int] = world.get_all_entities()

    assert len(entities_after_creation) == len(entities_before_creation) + 1, (
        "Player was not created"
    )


def test_create_world_returns_world() -> None:
    world: World = prefabs.create_empty_world()

    assert isinstance(world, World), "Incorrect type was returns by load_world()!"


def test_create_world_creates_new_instance() -> None:
    world1: World = prefabs.create_empty_world()
    world2: World = prefabs.create_empty_world()

    assert world1 is not world2
