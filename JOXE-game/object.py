import pygame   

class Object:
    def __init__(self, x, y, level, cell_size):
        self.x = x
        self.y = y
        self.level = level
        self.cell_size = cell_size

    def update_image_size(self, cell_size):
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image