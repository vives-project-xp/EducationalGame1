import pygame

class House:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.image = pygame.image.load('./assets/resources/houses/house1.png')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, surface):
        # Adjust the position so the house is centered at (x, y)
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)