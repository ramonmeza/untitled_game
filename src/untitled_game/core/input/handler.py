from .source import InputSource
from .states import InputState


class InputHandler:
    def __init__(self, input_source: InputSource) -> None:
        self._input_source: InputSource = input_source
        self._input_state: InputState = InputState()

    def get_input_state(self) -> InputState:
        return self._input_state

    def poll(self) -> None:
        self._input_source.set_input_state(self._input_state)
