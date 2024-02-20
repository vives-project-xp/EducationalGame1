import pygame

class Car:
    def __init__(self, grid_size, road_objects):
        self.grid_size = grid_size
        self.road_objects = road_objects
        self.current_road_index = 0  # Start from the first road
        self.speed = 5  # Adjust the speed as needed
        self.image = pygame.transform.scale(pygame.image.load('./assets/resources/cars/car.png'), (grid_size, grid_size))
        self.position = self.get_start_position()
        self.direction = 1

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
        road_start_x = road.x
        road_end_x = road.x + road_length

        if self.direction == 1 and self.position[0] < road_end_x:
            distance_to_move = min(self.speed, road_end_x - self.position[0])
            self.position = (self.position[0] + distance_to_move, self.position[1])
        elif self.direction == -1 and self.position[0] > road_start_x:
            distance_to_move = min(self.speed, self.position[0] - road_start_x)
            self.position = (self.position[0] - distance_to_move, self.position[1])
        else:
            # Change direction when reaching the end or the start of a road
            self.direction *= -1

            # Update the car's y position to the y position of the next or previous road
            if self.direction == 1:
                self.current_road_index = (self.current_road_index + 1) % len(self.road_objects)
            else:
                self.current_road_index = (self.current_road_index - 1) % len(self.road_objects)
            next_or_previous_road = self.road_objects[self.current_road_index]
            self.position = (self.position[0], next_or_previous_road.y)

    def draw(self, window):
        # Draw the car at its current position
        window.blit(self.image, self.position)
