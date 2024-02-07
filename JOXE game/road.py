import pygame

class Road:
    def __init__(self, x, y, grid_size):
        self.x = x - 10
        self.y = y - 8
        self.grid_size = grid_size

        # Load the road image and scale it slightly larger than the grid cell
        road_image = pygame.image.load('./assets/resources/road/road.png')
        self.image = pygame.transform.scale(road_image, (self.grid_size + 20, self.grid_size + 18))

    def draw(self, window):
        # Draw the road image at the given coordinates
        window.blit(self.image, (self.x, self.y))