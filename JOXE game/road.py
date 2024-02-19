import pygame

class Road:
    def __init__(self, x, y, grid_size):
        self.x = x - 10
        self.y = y - 8
        self.grid_size = grid_size
        self.type = None

        # Load the road image and scale it slightly larger than the grid cell
        road_image_path = './assets/resources/road/road.png'
        self.image = pygame.transform.scale(pygame.image.load(road_image_path), (self.grid_size + 20, self.grid_size + 18))

    def draw(self, window):
        # Draw the road image at the given coordinates
        window.blit(self.image, (self.x, self.y))

    def set_type(self, road_type):
        self.type = road_type

    def get_type(self):
        return self.type

    def get_road_image(self, col, row):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Road) and obj.x // self.grid_size == col and obj.y // self.grid_size == row:
                return obj.get_type()
        return '.'


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
