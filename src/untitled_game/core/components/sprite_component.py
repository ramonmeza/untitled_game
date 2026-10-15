from dataclasses import dataclass


@dataclass
class SpriteComponent:
    sprite_path: str
    zorder: int = 0


## Need to figure out how to get this component data to sprite rendering system
