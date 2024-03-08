import pygame
from object import Object

class Energy(Object):
    def __init__(self, x, y, grid_size, level=1):
        super().__init__(x, y, level)
        self.grid_size = grid_size
        self.image = pygame.image.load('./assets/resources/buildings/energy/windmills/windmillv2.png')
        self.image = pygame.transform.scale(self.image, (grid_size, grid_size))

    def draw(self, window):
        window.blit(self.image, (self.x * self.grid_size, self.y * self.grid_size))

    def update(self):
        pass 