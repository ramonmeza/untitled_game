from typing import Protocol


class InputController(Protocol):
    def get_input_vector(self) -> tuple[float, float]: ...
