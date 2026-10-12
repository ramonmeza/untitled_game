from typing import Protocol

from .actions import GameAction


class Controller(Protocol):
    """
    Used to connect hardware to the game. Would need an abstraction if we dont want to call raylib directly.
    Will have to think about how to abstract input, but this gives us a hook we could eventually refactor.
    """

    def poll_actions(self) -> list[GameAction]: ...
