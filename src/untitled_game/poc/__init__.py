from argparse import ArgumentParser

from .app import App
from .game import Game
from .input_controller import InputController
from .renderer import Renderer
from .window import Window

type Platform = tuple[Window, Renderer, InputController]


def create_platform(platform_name: str) -> Platform:
    match platform_name.lower():
        case "ascii":
            from .ascii import TerminalController, AsciiRenderer, AsciiWindow

            return AsciiWindow(), AsciiRenderer(), TerminalController()

        case "raylib":
            from .raylib import RaylibRenderer, RaylibWindow, RaylibController

            return RaylibWindow(), RaylibRenderer(), RaylibController()

        case _:
            raise NotImplementedError


parser = ArgumentParser()
parser.add_argument("--platform", choices=["ascii", "raylib"], default="raylib")
args = parser.parse_known_args()

chosen_platform: str = args[0].platform
platform: Platform = create_platform(chosen_platform)
app: App = App(platform[0], platform[1], Game(platform[2]))
app.run()
