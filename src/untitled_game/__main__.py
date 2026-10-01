import sys

from .application import Application
from .platforms.raylib import RaylibPlatform


def main() -> None:
    app: Application = Application(platform=RaylibPlatform())
    app.run()


sys.exit(main())
