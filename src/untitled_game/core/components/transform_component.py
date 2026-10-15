from dataclasses import dataclass, field

from .. import Vector2


@dataclass
class TransformComponent:
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: Vector2 = field(default_factory=Vector2)
