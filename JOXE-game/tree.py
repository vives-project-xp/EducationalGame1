import pygame

class Tree:
    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.image = pygame.image.load('./assets/resources/nature/tree1.png')
        self.image = pygame.transform.scale(self.image, (grid_size, grid_size))
        self.level = 0

    def draw(self, window):
        window.blit(self.image, (self.x * self.grid_size, self.y * self.grid_size))

    def update(self):
        pass
