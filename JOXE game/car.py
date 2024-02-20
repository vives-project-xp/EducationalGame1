import pygame

class Car:
    def __init__(self, grid_size, road_objects):
        self.grid_size = grid_size
        self.road_objects = road_objects
        self.current_road_index = 0  # Start from the first road
        self.speed = 5  # Adjust the speed as needed
        self.image = pygame.transform.scale(pygame.image.load('./assets/resources/cars/car.png'), (grid_size, grid_size))
        self.position = self.get_start_position()

    def get_start_position(self):
        # Get the starting position based on the first road
        if self.road_objects:
            first_road = self.road_objects[0]
            return (first_road.x, first_road.y)
        return (0, 0)

    def update(self):
        if self.road_objects:
            # Move the car along the current road
            current_road = self.road_objects[self.current_road_index]
            self.move_along_road(current_road)

    def move_along_road(self, road):
        road_length = self.grid_size + 20  # Adjust the road length
        if self.position[0] < road.x + road_length:
            self.position = (self.position[0] + self.speed, self.position[1])
        else:
            # Move to the next road when reaching the end of the current road
            self.current_road_index = (self.current_road_index + 1) % len(self.road_objects)
            self.position = (road.x, road.y)

    def draw(self, window):
        # Draw the car at its current position
        window.blit(self.image, self.position)
