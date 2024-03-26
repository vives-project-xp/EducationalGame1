import pygame
from zobjectfiles.object import Object

class Energy(Object):
    def __init__(self, x, y, grid_size, level=1, upgrade_cost=10000):
        super().__init__(x, y, level, grid_size)
        self.upgrade_cost = upgrade_cost
        self.grid_size = grid_size
        self.images = [f'./assets/resources/buildings/energy/windmills/windmill{i}.png' for i in range(1, 5)]
        self.image = self.load_image(self.images[self.level - 1], grid_size, grid_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def draw(self, window):
        window.blit(self.image, (self.x * self.grid_size, self.y * self.grid_size))

    def upgrade(self):
        if self.level < 4:
            self.level += 1
            self.image = self.load_image(self.images[self.level - 1], self.grid_size, self.grid_size)
