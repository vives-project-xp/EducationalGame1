import pygame
from object import Object

class Road(Object):
    def __init__(self, x, y, grid_size, level=0, rotation=0):
        super().__init__(x-10, y-10, level)
        self.grid_size = grid_size
        self.type = None
        self.scale = 1.28  #1.28
        self.rotation = rotation
        
        self.set_type('road')

    def draw(self, window):
        # Draw the road image at the given coordinates
        window.blit(self.image, (self.x, self.y))

    def set_type(self, road_type):
        self.type = road_type
        # Update the road image based on the new type
        self.update_image()

    def update_image(self):
        # Load the road image based on its type
        road_image_path = f'./assets/resources/road/{self.type}.png'
        image = pygame.image.load(road_image_path)

        # Calculate new size
        new_size = (int(self.grid_size * (self.scale + 0.1)), int(self.grid_size * (self.scale + 0.11)))

        # Scale the image
        self.image = pygame.transform.scale(image, new_size)

        # Apply rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, rotation)


        



