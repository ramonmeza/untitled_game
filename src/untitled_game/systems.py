from .camera import Camera
from .components import ControllerComponent, MovementComponent, PositionComponent
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
        movement_components: dict[int, MovementComponent],
        positions_components: dict[int, PositionComponent],
        controller_components: dict[int, ControllerComponent],
        delta_time: float,
    ) -> None:
        cls.time_since_start += delta_time

        for entity_id, movement_comp in movement_components.items():
            pos_comp = positions_components.get(entity_id, None)
            if pos_comp is None:
                continue

            controller_comp = controller_components.get(entity_id, None)
            if controller_comp is None:
                continue
            cls.apply_movement(pos_comp, controller_comp)

    @classmethod
    def apply_movement(
        cls,
        position_comp: PositionComponent,
        controller_comp: ControllerComponent,
    ) -> None:
        pass


class ActionSystem:
    @classmethod
    def update(cls, controller_components: dict[int, ControllerComponent]) -> None:
        for controller_comp in controller_components.values():
            controller_comp.actions = controller_comp.controller.poll_actions()
