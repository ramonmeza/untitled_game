from dataclasses import dataclass
from typing import Any, cast
from uuid import uuid1

from .components import (
    BoxComponent,
    ControllerComponent,
    MovementComponent,
    PositionComponent,
)

Components = BoxComponent | ControllerComponent | MovementComponent | PositionComponent
ComponentsTypes = (
    type[BoxComponent]
    | type[ControllerComponent]
    | type[MovementComponent]
    | type[PositionComponent]
)


@dataclass
class EntityComponentPair:
    entity_id: int
    component: Components


class ECS:
    """
    `entities` is a list of entity IDs (random numbers in our case)
    `components` is a dictionary whose keys are Component class types, and values are lists of tuples.
        These tuples are used to map the entity ID to the component data.

    Think of `components` as a structure which holds lists of key/value pairs for every component type.
    """

    def __init__(self) -> None:
        self.entities: list[int] = []
        self.components: dict[ComponentsTypes, list[EntityComponentPair]] = {}

    def generate_entity_id(self) -> int:
        return uuid1().int

    def create_entity(self) -> int:
        entity_id: int = self.generate_entity_id()
        self.entities.append(entity_id)
        return entity_id

    def add_component(
        self,
        entity_id: int,
        component_cls: ComponentsTypes,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        component: Components = component_cls(*args, **kwargs)
        if component_cls not in self.components:
            self.components[component_cls] = []
        self.components[component_cls].append(EntityComponentPair(entity_id, component))

    def get_components_of_type[T: Components](
        self, entity_id: int, component_cls: type[T]
    ) -> list[T]:
        return [
            component
            for component in self.get_components(entity_id)
            if isinstance(component, component_cls)
        ]

    def get_components(self, entity_id: int) -> list[Components]:
        pairs: list[EntityComponentPair] = [
            ecp for comp in self.components.values() for ecp in comp
        ]
        components: list[Components] = [
            pair.component for pair in pairs if pair.entity_id == entity_id
        ]
        return components

    def get_all_entities_with_components(self, *component_cls: ComponentsTypes) -> list[int]:
        found_entities: list[int] = []
        for entity_id in self.entities:
            components_types = [type(x) for x in self.get_components(entity_id)]
            if any(x for x in components_types if x in component_cls):
                found_entities.append(entity_id)

        return found_entities

    def get_all_components_of_type[T: Components](self, component_cls: type[T]) -> list[T]:
        return cast(list[T], [pair.component for pair in self.components[component_cls]])
