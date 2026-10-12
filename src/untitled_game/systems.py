from .camera import Camera
from .components import ControllerComponent, MovementComponent, PositionComponent
from .ecs import ECS
from .utils import vector2_lerp


class CameraFollowSystem:
    @staticmethod
    def update(camera: Camera, target: PositionComponent, delta_time: float) -> None:
        new_x, new_y = vector2_lerp(
            camera.position.x, camera.position.y, target.x, target.y, delta_time
        )
        camera.position.x = new_x
        camera.position.y = new_y


class MovementSystem:
    time_since_start: float = 0.0

    @classmethod
    def update(
        cls,
        ecs: ECS,
        movables: list[int],
        delta_time: float,
    ) -> None:
        cls.time_since_start += delta_time

        for entity_id in movables:
            _movement_comp = ecs.get_components_of_type(entity_id, MovementComponent)[0]
            position_comp = ecs.get_components_of_type(entity_id, PositionComponent)[0]
            controller_comp = ecs.get_components_of_type(entity_id, ControllerComponent)[0]
            cls.apply_movement(position_comp, controller_comp)

    @classmethod
    def apply_movement(
        cls,
        position_comp: PositionComponent,
        controller_comp: ControllerComponent,
    ) -> None:
        pass


class ActionSystem:
    @classmethod
    def update(cls, controller_components: list[ControllerComponent]) -> None:
        for controller_comp in controller_components:
            controller_comp.actions = controller_comp.controller.poll_actions()
