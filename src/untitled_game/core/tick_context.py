from dataclasses import dataclass

from .input import InputState


@dataclass
class TickContext:
    delta_time: float
    input_state: InputState
