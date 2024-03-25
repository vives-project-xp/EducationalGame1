import pygame
from object import Object

class Tree(Object):
    def __init__(self, x, y, grid_size, level=0):
        super().__init__(x, y, level, grid_size)
        self.grid_size = grid_size
        self.images = [f'./assets/resources/nature/tree{i}.png' for i in range(1, 4)]
        self.image = self.load_image(self.images[self.level], grid_size, grid_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def update_position(self, new_grid_size):
        self.x = self.x / self.grid_size * new_grid_size
        self.y = self.y / self.grid_size * new_grid_size
        self.grid_size = new_grid_size
        self.image = self.load_image(self.images[self.level], new_grid_size, new_grid_size)

    def draw(self, window):
        window.blit(self.image, (self.x * self.grid_size, self.y * self.grid_size))

    def catch_fire(self):
        self.image = self.load_image('./assets/resources/nature/fire.png', self.grid_size, self.grid_size)

    def upgrade(self):
        if self.level < 2:
            self.level += 1
            self.image = self.load_image(self.images[self.level], self.grid_size, self.grid_size)

    def update(self):
        pass