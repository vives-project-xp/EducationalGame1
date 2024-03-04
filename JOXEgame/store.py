import pygame

class Store:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.image = pygame.image.load('./assets/resources/buildings/stores/store.png')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.level = 1
        self.upgrade_cost = 5000
        self.ecoscore_bonus = -5

    def draw(self, surface):
        # Adjust the position so the store is centered at (x, y)
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def upgrade(self):
        if self.level < 4:
            self.level += 1
            self.upgrade_cost *= 2  # You can adjust the upgrade cost formula as needed
            self.ecoscore_bonus += 1  # You can adjust the eco score bonus as needed
