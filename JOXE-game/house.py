import pygame
from object import Object

class House(Object):
    def __init__(self, x, y, cell_size, level=1, upgrade_cost=1000, version=1):
        super().__init__(x, y, level, cell_size)
        self.inhabitants = 0 
        self.version = version
        self.upgrade_cost = upgrade_cost
        self.inhab_happiness = 0
        self.ecoscore = -1
        self.images = [f'./assets/resources/houses/house{self.version}{i}.png' for i in range(1, 10)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def change_version(self, version):
        self.version = version
        self.images = [f'./assets/resources/houses/house{self.version}{i}.png' for i in range(1, 10)]
        self.image = self.load_image(self.images[self.level - 1], self.cell_size, self.cell_size)

    def draw(self, surface):
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def add_inhabitant(self, amount):
        self.inhabitants += amount

    def update_happiness(self, amount):
        self.inhab_happiness += amount
    
    def upgrade(self):
        if self.level < 9:
            self.level += 1
            self.upgrade_cost = (5**self.level)*1000