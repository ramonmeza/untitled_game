from .core.application import Application
from .core.factories import create_window
from .core.window import Window

APP_NAME: str = "Untitled Game"


def main() -> None:
    window: Window = create_window(APP_NAME)
    app: Application = Application(window)
    app.run()


main()
