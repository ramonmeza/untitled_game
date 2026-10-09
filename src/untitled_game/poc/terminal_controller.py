import msvcrt


class TerminalController:
    def get_input_vector(self) -> tuple[float, float]:
        NO_INPUT: tuple[float, float] = (0.0, 0.0)

        if not msvcrt.kbhit():  # key pressed?
            return NO_INPUT

        key = msvcrt.getch()
        if key not in (b"\x00", b"\xe0"):  # windows: arrow keys are 2 bytes
            return NO_INPUT

        key = msvcrt.getch()  # reads second byte

        return {
            b"H": (0, -1),  # up
            b"P": (0, 1),  # down
            b"K": (-1, 0),  # left
            b"M": (1, 0),  # right
        }.get(key, NO_INPUT)
