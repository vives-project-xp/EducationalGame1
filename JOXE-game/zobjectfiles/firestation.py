import pygame
from zobjectfiles.object import Object

class Firestation(Object):
    def __init__(self, x, y, cell_size, level=1, upgrade_cost=100000):
        super().__init__(x, y, level, cell_size, 5, 1000)
        self.upgrade_cost = upgrade_cost
        self.ecoscore = -1
        # Range of the hospital
        self.effect_range = 3
        self.images = [f'./assets/resources/buildings/firestation/firestation{i}.png' for i in range(1, 10)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def draw(self, surface):
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def higher_effect_range(self, amount):
        self.effect_range += amount

    def gamestate_update_effect_range(self):
        self.effect_range = self.effect_range + self.level
    
    def upgrade(self):
        if self.level < 9:
            self.level += 1
            for i in range(self.level):
                self.upgrade_cost = (5**i)*20000