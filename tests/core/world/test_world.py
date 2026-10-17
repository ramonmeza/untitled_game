from untitled_game.core.world.world import World


def test_world_get_all_entities() -> None:
    from untitled_game.core.components.transform_component import TransformComponent

    world: World = World()
    assert len(world.get_all_entities()) == 0

    test_entity = world.create_entity(TransformComponent)
    assert len(world.get_all_entities()) == 1

    another_test_entity = world.create_entity()
    assert len(world.get_all_entities()) == 2

    assert world.get_all_entities() == [test_entity, another_test_entity]

    world.destroy_entity(test_entity)
    assert len(world.get_all_entities()) == 1


def test_destroy_entity_with_invalid_entity_id() -> None:
    world: World = World()
    INVALID_ENTITY_ID: int = 999
    world.destroy_entity(INVALID_ENTITY_ID)


def test_destroy_entity_with_no_components() -> None:
    world: World = World()
    test_entity = world.create_entity()
    world.destroy_entity(test_entity)


def test_destroy_entity_with_components() -> None:
    from untitled_game.core.components import SpriteComponent, TransformComponent

    world: World = World()

    test_entity = world.create_entity(SpriteComponent("sprite_path"), TransformComponent())
    assert test_entity in world.get_all_entities()
    world.destroy_entity(test_entity)
    assert test_entity not in world.get_all_entities()

    test_entity = world.create_entity(TransformComponent())
    assert test_entity in world.get_all_entities()
    world.destroy_entity(test_entity)
    assert test_entity not in world.get_all_entities()

    test_entity = world.create_entity()
    assert test_entity in world.get_all_entities()
    world.destroy_entity(test_entity)
    assert test_entity not in world.get_all_entities()


def test_get_component_from_entity_with_no_components() -> None:
    from untitled_game.core.components import TransformComponent

    world: World = World()

    test_entity = world.create_entity()
    component = world.get_component_by_type(test_entity, TransformComponent)
    assert component is None


def test_get_component_from_entity_with_components() -> None:
    from untitled_game.core.components import SpriteComponent, TransformComponent

    world: World = World()

    test_entity = world.create_entity(SpriteComponent("sprite_path"), TransformComponent())
    component = world.get_component_by_type(test_entity, TransformComponent)
    assert isinstance(component, TransformComponent)


def test_query_empty_world() -> None:
    from untitled_game.core.components import TransformComponent

    world: World = World()
    query = world.query_by_component_types(TransformComponent)
    assert query == []


def test_query_world_with_one_entity_with_no_components() -> None:
    from untitled_game.core.components import TransformComponent

    world: World = World()
    entity = world.create_entity()
    query = world.query_by_component_types(TransformComponent)

    assert query == []
    assert entity in world.get_all_entities()


def test_query_world_with_one_entity_with_no_matching_components() -> None:
    from untitled_game.core.components import SpriteComponent, TransformComponent

    world: World = World()
    entity = world.create_entity(SpriteComponent("sprite_path"))
    query = world.query_by_component_types(TransformComponent)

    assert query == []
    assert entity in world.get_all_entities()


def test_query_world_with_one_entity_with_matching_component() -> None:
    from untitled_game.core.components import TransformComponent

    world: World = World()
    entity = world.create_entity(TransformComponent())
    query = world.query_by_component_types(TransformComponent)

    assert query == [entity]
    assert entity in world.get_all_entities()


def test_query_two_components_with_world_with_many_entities() -> None:
    from untitled_game.core.components import SpriteComponent, TransformComponent

    world: World = World()
    entity1 = world.create_entity(TransformComponent())
    world.create_entity(SpriteComponent("sprite_path"))
    entity2 = world.create_entity(TransformComponent(), SpriteComponent("sprite_path"))
    world.create_entity(SpriteComponent("sprite_path"))
    entity3 = world.create_entity(SpriteComponent("sprite_path"), TransformComponent())
    entity4 = world.create_entity(TransformComponent())
    query = world.query_by_component_types(TransformComponent, SpriteComponent)

    assert query == [entity2, entity3]
    assert entity1 in world.get_all_entities()
    assert entity2 in world.get_all_entities()
    assert entity3 in world.get_all_entities()
    assert entity4 in world.get_all_entities()
