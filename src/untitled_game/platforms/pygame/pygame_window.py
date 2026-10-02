import pygame


class PygameWindow:
    def open_window(self, width: int, height: int, title: str) -> None:
        pygame.display.set_mode(size=(width, height))
        pygame.display.set_caption(title)

    def is_open(self) -> bool:
        return pygame.display.get_init()

    def close_window(self) -> None:
        pygame.display.get_active()
