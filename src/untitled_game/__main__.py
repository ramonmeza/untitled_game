import sys

from .application import Application
from .game.untitled_game import UntitledGame
from .platforms.raylib import RaylibPlatform


def main() -> None:
    app: Application = Application(platform=RaylibPlatform(), game=UntitledGame())
    app.run()


sys.exit(main())
