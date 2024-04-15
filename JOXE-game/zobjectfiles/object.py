import pygame   

class Object:
    def __init__(self, x, y, level, cell_size, eco_change=0, money_change=0):
        self.x = x
        self.y = y
        self.level = level
        self.eco_change = eco_change
        self.money_change = money_change
        self.cell_size = cell_size

    def update_image_size(self, cell_size):
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