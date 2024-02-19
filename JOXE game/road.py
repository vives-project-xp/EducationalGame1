import pygame

class Road:
    def __init__(self, x, y, grid_size):
        self.x = x - 10
        self.y = y - 8
        self.grid_size = grid_size
        self.type = None

        # Load the default road image
        self.set_type('road')

    def draw(self, window):
        # Draw the road image at the given coordinates
        window.blit(self.image, (self.x, self.y))

    def set_type(self, road_type):
        self.type = road_type
        # Update the road image based on the new type
        self.update_image()

    def update_image(self):
        # Load the road image based on its type and scale it
        road_image_path = f'./assets/resources/road/{self.type}.png'
        self.image = pygame.transform.scale(pygame.image.load(road_image_path), (self.grid_size + 20, self.grid_size + 18))

    def change_image(self, new_image_path):
        # Change the road image to the specified image
        self.type = 'v-road'
        self.update_image()



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
