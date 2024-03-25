import pygame
from object import Object

class Store(Object):
    def __init__(self, x, y, cell_size, level=1, upgrade_cost=3000):
        super().__init__(x, y, level, cell_size)
        self.upgrade_cost = upgrade_cost
        self.ecoscore_bonus = -5
        self.images = [f'./assets/resources/buildings/stores/store{i}.png' for i in range(1, 5)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def update_position(self, new_cell_size):
        self.x = self.x / self.cell_size * new_cell_size
        self.y = self.y / self.cell_size * new_cell_size
        self.cell_size = new_cell_size
        self.update_image_size(new_cell_size)

    def draw(self, surface):
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def upgrade(self):
        if self.level < 4:
            self.level += 1
            self.upgrade_cost = (5**(self.level-1))*3000
            self.ecoscore_bonus += 1  # You can adjust the eco score bonus as needed
            self.image = self.load_image(self.images[self.level - 1], self.image.get_width(), self.image.get_height())
