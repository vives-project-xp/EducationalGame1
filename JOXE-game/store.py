import pygame

class Store:
    def __init__(self, x, y, cell_size, level=1):
        self.x = x
        self.y = y
        self.level = level
        self.upgrade_cost = 5000
        self.ecoscore_bonus = -5
        self.images = [f'./assets/resources/buildings/stores/store{i}.png' for i in range(1, 5)]
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def draw(self, surface):
        # Adjust the position so the store is centered at (x, y)
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)

    def upgrade(self):
        if self.level < 4:
            self.level += 1
            self.upgrade_cost *= 2  # You can adjust the upgrade cost formula as needed
            self.ecoscore_bonus += 1  # You can adjust the eco score bonus as needed
            self.image = self.load_image(self.images[self.level - 1], self.image.get_width(), self.image.get_height())