import pygame

class Road:
    def __init__(self, x, y, grid_size):
        self.x = x - 10
        self.y = y - 8
        self.grid_size = grid_size
        self.type = None

        # Load the road image and scale it slightly larger than the grid cell
        road_image = pygame.image.load('./assets/resources/road/road.png')
        self.image = pygame.transform.scale(road_image, (self.grid_size + 20, self.grid_size + 18))

    def draw(self, window):
        # Draw the road image at the given coordinates
        window.blit(self.image, (self.x, self.y))

    def get_road_type(self, neighbors):
        if neighbors == [1, 1, 0, 0]:
            return 'horizontal'
        elif neighbors == [0, 0, 1, 1]:
            return 'vertical'
        elif neighbors == [1, 1, 1, 0]:
            return 't_point'
        elif neighbors == [1, 1, 1, 1]:
            return 'x_point'
        else:
            return 'corner'


class Intersection:
    def __init__(self, x, y, grid_size, road_type):
        self.x = x - 10
        self.y = y - 8
        self.grid_size = grid_size
        self.road_type = road_type

        # Load the intersection image based on road type
        intersection_image_path = f'./assets/resources/road/{road_type}_intersection.png'
        self.image = pygame.transform.scale(pygame.image.load(intersection_image_path), (self.grid_size + 20, self.grid_size + 18))

    def draw(self, window):
        # Draw the intersection image at the given coordinates
        window.blit(self.image, (self.x, self.y))
