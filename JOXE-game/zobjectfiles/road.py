import pygame
from zobjectfiles.object import Object

class Road(Object):
    def __init__(self, x, y, grid_size, level=0, rotation=0):
        super().__init__(x-10, y-10, level, grid_size)
        self.grid_size = grid_size
        self.type = None
        self.scale = 1.28 
        self.rotation = rotation
        
        self.set_type('road')

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def set_type(self, road_type):
        self.type = road_type
        self.update_image()

    def update_image(self):
        road_image_path = f'./assets/resources/road/{self.type}.png'
        image = pygame.image.load(road_image_path)

        new_size = (int(self.grid_size * (self.scale + 0.1)), int(self.grid_size * (self.scale + 0.11)))

        self.image = pygame.transform.scale(image, new_size)

        self.image = pygame.transform.rotate(self.image, self.rotation)

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, rotation)
