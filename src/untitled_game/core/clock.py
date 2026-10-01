from typing import Protocol


class Clock(Protocol):
    def get_delta_time(self) -> float: ...
