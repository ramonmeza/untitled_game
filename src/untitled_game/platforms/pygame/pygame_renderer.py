import pygame


class PygameRenderer:
    def begin_frame(self) -> None:
        pass

    def clear_frame(self) -> None:
        screen = pygame.display.get_surface()
        screen.fill(pygame.Color("black"))

    def end_frame(self) -> None:
        pygame.display.flip()
