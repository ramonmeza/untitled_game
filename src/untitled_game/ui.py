from dataclasses import dataclass, field

import pyray as raylib


@dataclass
class UIStyle:
    font_color: raylib.Color = field(default=raylib.WHITE)
    bar_height: int = 12
    bar_width: int = 100
    font_size: int = 12
    vspacing: int = 2
    vpadding: int = 4
    hpadding: int = 6
