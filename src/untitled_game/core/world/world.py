from typing import cast

type EntityId = int


class World:
    STARTING_ENTITY_ID: int = 1

    def __init__(self) -> None:
        self._next_entity_id: EntityId = World.STARTING_ENTITY_ID
        self._entities: list[EntityId] = []
        self._components: dict[type, dict[EntityId, object]] = {}

    def get_all_entities(self) -> list[EntityId]:
        return self._entities.copy()

    def create_entity(self, *components: object) -> EntityId:
        entity_id: EntityId = self._next_entity_id
        self._entities.append(entity_id)
        self._next_entity_id += 1

        for component in components:
            component_type: type = type(component)
            if component_type not in self._components:
                self._components[component_type] = {}

            self._components[component_type][entity_id] = component

        return entity_id

    def destroy_entity(self, entity_id: EntityId) -> None:
        for component_instances in self._components.values():
            if entity_id not in component_instances:
                continue

            component_instances.pop(entity_id)

    def get_component[T: type](self, entity_id: EntityId, comp_type: T) -> T | None:
        component_map = self._components.get(comp_type, None)
        if component_map is None:
            return None

        component: object | None = component_map.get(entity_id, None)
        return cast(T, component) if component is not None else None

    def query(self, *components: object) -> list[EntityId]:
        all_entities_with_components: list[list[EntityId]] = [
            list(component_instances.keys())
            for component_type, component_instances in self._components.items()
            if component_type in components
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
