from typing import cast

type EntityId = int
type Component = object
type ComponentKey = str
type EntityComponentMapping = dict[EntityId, Component]


class World:
    STARTING_ENTITY_ID: EntityId = 1

    def __init__(self) -> None:
        self._next_entity_id: EntityId = World.STARTING_ENTITY_ID
        self._entities: list[EntityId] = []
        self._components: dict[ComponentKey, EntityComponentMapping] = {}

    def get_all_entities(self) -> list[EntityId]:
        return self._entities.copy()

    def create_entity(self, *components: Component) -> EntityId:
        entity_id: EntityId = self._next_entity_id
        self._entities.append(entity_id)
        self._next_entity_id += 1

        for component in components:
            self.add_component_to_entity(entity_id, component)

        return entity_id

    def add_component_to_entity(self, entity_id: EntityId, component: Component) -> None:
        component_key: ComponentKey = self._get_component_key(component)
        if component_key not in self._components:
            self._components[component_key] = {}

        self._components[component_key][entity_id] = component

    def destroy_entity(self, entity_id: EntityId) -> None:
        if entity_id not in self._entities:
            return

        for component_instances in self._components.values():
            if entity_id not in component_instances:
                continue

            component_instances.pop(entity_id)

        self._entities.remove(entity_id)

    def _get_component_key(self, component: Component) -> ComponentKey:
        return component.__class__.__name__

    def get_component_by_type[T](self, entity_id: EntityId, component_cls: type[T]) -> T | None:
        mapping: EntityComponentMapping | None = self._components.get(component_cls.__name__, None)
        if mapping is None:
            return None

        component: Component | None = mapping.get(entity_id, None)
        return cast(T, component)

    def query_by_component_types(self, *components: type[Component]) -> list[EntityId]:
        all_entities_with_components: list[list[EntityId]] = [
            list(entity_comp_map.keys())
            for component_key, entity_comp_map in self._components.items()
            if component_key in [component.__name__ for component in components]
        ]

        found_entities: list[EntityId] = []
        if len(all_entities_with_components) == 0:
            found_entities = []
        elif len(all_entities_with_components) == 1:
            found_entities = list(set(all_entities_with_components[0]))
        else:
            found_entities = list(
                set(all_entities_with_components[0]).intersection(*all_entities_with_components[1:])
            )
        return found_entities
