import pygame

class House:
    def __init__(self, x, y, cell_size, level=1):
        self.x = x
        self.y = y
        self.image = pygame.image.load('./assets/resources/houses/house1.png')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.inhabitants = 0 
        self.level = level
        self.upgrade_cost = 1000
        self.ecoscore = -1

    def draw(self, surface):
        # Adjust the position so the house is centered at (x, y)
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def add_inhabitant(self, amount):
        self.inhabitants += amount
    
    def upgrade(self):
            if self.level < 9:
                self.level += 1
                self.upgrade_cost *= 5  