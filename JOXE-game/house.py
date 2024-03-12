import pygame
from object import Object

class House(Object):
    def __init__(self, x, y, cell_size, level=1, upgrade_cost=1000):
        super().__init__(x, y, level)
        self.inhabitants = 0 
        self.cell_size = cell_size
        self.upgrade_cost = upgrade_cost
        self.ecoscore = -1
        self.images = [f'./assets/resources/houses/house{i}.png' for i in range(1, 10)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def update_position(self, new_cell_size):
        self.x = self.x / self.cell_size * new_cell_size
        self.y = self.y / self.cell_size * new_cell_size
        self.cell_size = new_cell_size
        self.update_image_size(new_cell_size)

    def update_image_size(self, cell_size):
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)
        

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def draw(self, surface):
        # Adjust the position so the house is centered at (x, y)
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def add_inhabitant(self, amount):
        self.inhabitants += amount
    
    def upgrade(self):
        if self.level < 9:
            self.level += 1
            for i in range(self.level):
                self.upgrade_cost = (5**i)*1000