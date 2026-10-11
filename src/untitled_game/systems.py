from .components import PositionComponent
from .core import Camera
from .utils import vector2_lerp


class CameraFollowSystem:
    @staticmethod
    def update(camera: Camera, target: PositionComponent, delta_time: float) -> None:
        new_x, new_y = vector2_lerp(
            camera.position.x, camera.position.y, target.x, target.y, delta_time
        )
        camera.position.x = new_x
        camera.position.y = new_y
