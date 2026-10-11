from .components import MovementComponent, MovementStyle, PositionComponent
from .core import Camera
from .utils import sine, vector2_lerp


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
        delta_time: float,
    ) -> None:
        cls.time_since_start += delta_time

        for entity_id, movement_comp in movement_components.items():
            pos_comp = positions_components.get(entity_id, None)
            if pos_comp is None:
                continue
            cls.apply_movement(movement_comp.movement_style, pos_comp)

    @classmethod
    def apply_movement(
        cls, movement_style: MovementStyle, position_comp: PositionComponent
    ) -> None:
        match movement_style:
            case MovementStyle.SINE:
                sine_amp: float = 200.0
                position_comp.y = sine(cls.time_since_start) * sine_amp
            case _:
                raise NotImplementedError
