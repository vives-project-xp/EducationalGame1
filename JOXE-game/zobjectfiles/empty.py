import pygame
from zobjectfiles.object import Object

class Empty(Object):
    def __init__(self, x, y, cell_size, level=1):
        super().__init__(x, y, level, cell_size)
        self.images = [f'./assets/resources/emptycell/emptycell.png']
        self.image = self.load_image(self.images[self.level - 1], cell_size, cell_size)

    def load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        image.set_alpha(0)  # Set opacity to 0
        return image

    def draw(self, surface):
        pos = (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2)
        surface.blit(self.image, pos)
