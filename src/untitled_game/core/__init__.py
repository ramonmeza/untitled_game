from dataclasses import dataclass


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0


__all__: list[str] = ["Vector2"]
