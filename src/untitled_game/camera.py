from dataclasses import dataclass, field

from .components import PositionComponent


@dataclass
class Camera:
    position: PositionComponent = field(default_factory=PositionComponent)
    zoom: float = 1.0
