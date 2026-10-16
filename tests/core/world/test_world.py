import untitled_game.core.world.world as test_module


def test_world_get_all_entities() -> None:
    world: test_module.World = test_module.World()
    assert len(world.get_all_entities()) == 0

    test_entity = world.create_entity()
    assert len(world.get_all_entities()) == 1

    another_test_entity = world.create_entity()
    assert len(world.get_all_entities()) == 2

    assert world.get_all_entities() == [test_entity, another_test_entity]

    world.destroy_entity(test_entity)
    assert len(world.get_all_entities()) == 1
