import pygame

class Grid: 
    def __init__(self, window, WIDTH, HEIGHT, GRID_SIZE):
        self.window = window
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_SIZE = GRID_SIZE

    def draw_grid(self):
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.window, (200, 200, 200), (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.window, (200, 200, 200), (0, y), (self.WIDTH, y))