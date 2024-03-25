import pygame
from object import Object

class Tree(Object):
    def __init__(self, x, y, cell_size, level=1, upgrade_cost=1000):
        super().__init__(x, y, level, cell_size)
        self.grid_size = cell_size
        self.upgrade_cost = upgrade_cost
        self.effect_range = 1
        self.images = [f'./assets/resources/nature/tree/tree{i}.png' for i in range(1, 4)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def draw(self, window):
        window.blit(self.image, (self.x * self.grid_size, self.y * self.grid_size))

    def higher_effect_range(self, amount):
        self.effect_range += amount

    def catch_fire(self):
        self.image = self.load_image('./assets/resources/nature/fire.png', self.grid_size, self.grid_size)

    def upgrade(self):
        if self.level <= 3:
            self.level += 1
            self.image = self.load_image(self.images[self.level-1], self.grid_size, self.grid_size)
            self.upgrade_cost = (5**self.level)*200
