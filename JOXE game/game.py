from grid import Grid
from gamestate import Gamestate
from house import House  # Make sure to import the House class
import pygame
import os
import sys

class Game:
    def __init__(self, window, width, height, grid_size, game_state=None):
        self.window = window
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.game_state = Gamestate()
        self.font = pygame.font.Font(None, 36)
        self.grid = Grid(window, width, height, grid_size, self.game_state, self.font)

    def draw(self):
        self.grid.draw_grid()

        if self.game_state.climateScore <= 0:
            self.draw_game_over()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    def handle_click(self, x, y):
        self.game_state.add_house(1)
        self.game_state.add_citizen(5)
        self.game_state.remove_money(1000)
        self.game_state.remove_climate_score(5)
        # Convert the position to grid coordinates
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size

        # Create a new House object at the clicked position
        house = House(grid_x * self.grid_size, grid_y * self.grid_size, self.grid_size)

        # Add the new House object to the game state
        self.game_state.placed_objects.append(house)

    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, (255, 0, 0))
        text2 = font2.render('You have destroyed the climate!', 1, (255, 0, 0))
        self.window.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        self.window.blit(text2, (self.width//2 - text2.get_width()//2, self.height//2 + text.get_height()//2))