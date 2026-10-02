import pygame


class PygameDrawingAPI:
    def draw_circle(self, x: int, y: int, radius: float, color: tuple[int, int, int, int]) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.circle(surface=screen, color=color, center=(x, y), radius=radius)
