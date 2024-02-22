import pygame
import random

class Car:
    def __init__(self, grid_size, road_objects):
        self.grid_size = grid_size
        self.road_objects = road_objects
        self.current_road_index = 0  # Start from the first road
        self.speed = 5  # Adjust the speed as needed
        self.scale = 0.05  # Adjust the scale as needed
        self.offset = 3  # Adjust the offset as needed
        self.visible = False  # The car is initially invisible

        # Load the image
        image = pygame.image.load('./assets/resources/cars/car.png')
        # Calculate new size
        width, height = image.get_size()
        new_size = (int(width * self.scale), int(height * self.scale))
        # Scale the image
        self.image = pygame.transform.scale(image, new_size)

        self.position = self.get_start_position()

    def get_start_position(self):
        # Get the starting position based on the first road
        if self.road_objects:
            first_road = self.road_objects[0]
            middle_y = first_road.y + (self.grid_size / 2) - (self.image.get_height() / 2) + self.offset
            return (first_road.x, middle_y)
        return (0, 0)

    def update(self):
        if self.road_objects:
            # If the car is not visible and there are road objects, make the car visible and choose a random road
            if not self.visible and len(self.road_objects) > 0:
                self.visible = True
                self.choose_random_road()

            # If the car is visible, move it along the current road
            if self.visible:
                current_road = self.road_objects[self.current_road_index]
                self.move_along_road(current_road)

    def choose_random_road(self):
        # Choose a random road from the list of road objects
        self.current_road_index = random.randint(0, len(self.road_objects) - 1)

        # Update the car's position to the start of the chosen road
        chosen_road = self.road_objects[self.current_road_index]
        middle_y = chosen_road.y + (self.grid_size / 2) - (self.image.get_height() / 2) + self.offset
        self.position = (chosen_road.x, middle_y)

    def move_along_road(self, road):
        road_length = self.grid_size + 20  # Adjust the road length
        road_end_x = road.x + road_length

        if self.position[0] < road_end_x:
            distance_to_move = min(self.speed, road_end_x - self.position[0])
            self.position = (self.position[0] + distance_to_move, self.position[1])
        else:
            # Move to the next road when reaching the end of the current road
            self.current_road_index = (self.current_road_index + 1) % len(self.road_objects)

            if self.current_road_index == 0:  # If the car has reached the end of the final road
                # Reset the car's position to the start of the first road
                first_road = self.road_objects[0]
                middle_y = first_road.y + (self.grid_size / 2) - (self.image.get_height() / 2) + self.offset
                self.position = (first_road.x, middle_y)
            else:
                next_road = self.road_objects[self.current_road_index]  # Get the next road

                # Gradually change the car's x position to the x position of the next road
                if self.position[0] < next_road.x:
                    self.position = (self.position[0] + 1, self.position[1])
                elif self.position[0] > next_road.x:
                    self.position = (self.position[0] - 1, self.position[1])

                # Update the car's y position to the middle of the next road
                middle_y = next_road.y + (self.grid_size / 2) - (self.image.get_height() / 2) + self.offset
                self.position = (self.position[0], middle_y)

    def draw(self, window):
        # Only draw the car if it is visible
        if self.visible:
            window.blit(self.image, self.position)