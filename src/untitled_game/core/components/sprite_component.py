from dataclasses import dataclass


@dataclass
class SpriteComponent:
    sprite_path: str
    zorder: int = 0
