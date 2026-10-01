import pyray as raylib


class RaylibClock:
    def get_delta_time(self) -> float:
        return raylib.get_frame_time()
