from typing import Protocol

from .states import InputState


class InputSource(Protocol):
    def set_input_state(self, state: InputState) -> None: ...
