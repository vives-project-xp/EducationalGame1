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
        self.selected_cell = None
        self.menu_bar_visible = False
        house_image = pygame.image.load('./assets/resources/houses/house1.png')
        self.house_image = pygame.transform.scale(house_image, (80, 80))

    def draw(self):
        self.grid.draw_grid()

        if self.menu_bar_visible:
            self.draw_menu_bar()

        # End the game if climateScore is 0 or lower
        if self.game_state.climateScore <= 0:
            self.draw_game_over()
            pygame.display.update()
            pygame.time.wait(3000)  # wait for 3 seconds
            pygame.quit()
            sys.exit()

    def draw_menu_bar(self):
        # Draw the menu bar at the bottom of the screen
        pygame.draw.rect(self.window, (200, 200, 200), (0, self.height - 100, self.width, 100))

        # Draw the house image on the menu bar
        self.window.blit(self.house_image, (10, self.height - 80))


    def handle_click(self, x, y):
        if self.menu_bar_visible:
            # If the menu bar is visible, check if the house image was clicked
            if self.height - 80 <= y <= self.height - 10 and 10 <= x <= 90:
                # Add a house to the selected cell
                self.game_state.objects.append(House(self.selected_cell))
                self.menu_bar_visible = False
        else:
            # If the menu bar is not visible, show it and store the selected cell
            self.menu_bar_visible = True
            self.selected_cell = (x // self.grid_size, y // self.grid_size)


    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, (255, 0, 0))
        text2 = font2.render('You have destroyed the climate!', 1, (255, 0, 0))
        self.window.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        self.window.blit(text2, (self.width//2 - text2.get_width()//2, self.height//2 + text.get_height()//2))