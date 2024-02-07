from grid import Grid
from gamestate import Gamestate
from house import House 
from road import Road
import pygame
import os
import sys
import random

class Game:
    def __init__(self, window, width, height, grid_size, game_state=None):
        self.window = window
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.game_state = Gamestate()
        self.font = pygame.font.Font(None, 36)
        self.grid = Grid(window, width, height, grid_size, self.game_state, self.font)
        self.selected_cell = None
        self.menu_bar_visible = False
        self.occupied_cells = set()

        house_image = pygame.image.load('./assets/resources/houses/house1.png')
        self.house_image = pygame.transform.scale(house_image, (80, 80))

        road_image = pygame.image.load('./assets/resources/road/road.png')
        self.road_image = pygame.transform.scale(road_image, (80, 80))

    def draw(self):
        self.grid.draw_grid()

        if self.menu_bar_visible:
            self.draw_menu_bar()

            # If a cell is selected, draw a yellow outline around it
            if self.selected_cell is not None:
                pygame.draw.rect(self.window, (255, 255, 0), (self.selected_cell[0], self.selected_cell[1], self.grid_size, self.grid_size), 2)

        # End the game if climateScore is 0 or lower
        if self.game_state.climateScore <= 0:
            self.draw_game_over()
            pygame.display.update()
            pygame.time.wait(3000)  # wait for 3 seconds
            pygame.quit()
            sys.exit()

    def draw_menu_bar(self):
        # Draw the menu bar background
        pygame.draw.rect(self.window, (230, 230, 230), (0, self.height - 80, self.width, 80))

        # Draw the house and road images
        self.window.blit(self.house_image, (10, self.height - 70))
        self.window.blit(self.road_image, (100, self.height - 70))

        # Draw the cost text
        font = pygame.font.Font(None, 24)  # Create a font object
        house_cost_text = font.render("$1000", True, (0, 0, 0))  # Create a Surface with the house cost text
        road_cost_text = font.render("$50", True, (0, 0, 0))  # Create a Surface with the road cost text
        self.window.blit(house_cost_text, (60, self.height - 70))  # Draw the house cost text
        self.window.blit(road_cost_text, (150, self.height - 70))  # Draw the road cost text

    def handle_click(self, x, y):
        # Convert the mouse click coordinates to grid coordinates
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size

        # Convert grid coordinates back to pixel coordinates
        pixel_x = grid_x * self.grid_size
        pixel_y = grid_y * self.grid_size

        if self.menu_bar_visible:
            # If the menu bar is visible, check if the house or road image was clicked
            if self.height - 80 <= y <= self.height - 10:
                if 10 <= x <= 90:
                    # House image was clicked
                    if self.selected_cell is not None and self.game_state.money >= 1000:
                        house = House(self.selected_cell[0], self.selected_cell[1], self.grid_size)
                        self.game_state.placed_objects.append(house)
                        self.game_state.remove_money(1000)
                        self.game_state.add_citizen(random.randint(3, 6))
                        self.game_state.add_house(1)
                        self.selected_cell = None  # Clear the selected cell
                    self.menu_bar_visible = False
                elif 100 <= x <= 180:
                    # Road image was clicked
                    if self.selected_cell is not None and self.game_state.money >= 50:
                        road = Road(self.selected_cell[0], self.selected_cell[1], self.grid_size)
                        self.game_state.placed_objects.append(road)
                        self.game_state.remove_money(50)
                        self.game_state.remove_climate_score(1)
                        self.selected_cell = None
                    self.menu_bar_visible = False
            else:
                # If the click was outside the menu bar, close the menu
                self.menu_bar_visible = False
                self.selected_cell = None  # Clear the selected cell
        else:
            # If the menu bar is not visible, show it and store the selected cell
            if (grid_x, grid_y) not in self.occupied_cells:
                self.menu_bar_visible = True
                self.selected_cell = (pixel_x, pixel_y)
                self.occupied_cells.add((grid_x, grid_y))  # Mark the cell as occupied

    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, (255, 0, 0))
        text2 = font2.render('You have destroyed the climate!', 1, (255, 0, 0))
        self.window.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        self.window.blit(text2, (self.width//2 - text2.get_width()//2, self.height//2 + text.get_height()//2))