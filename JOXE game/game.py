from grid import Grid
from gamestate import Gamestate
from house import House
from road import Road
from energy import Energy
import pygame
import os
import sys
import random

class Game:
    COLORS = {
        'white': (255, 255, 255),
        'yellow': (255, 255, 0),
        'menu_background': (230, 230, 230),
        'game_over_text': (255, 0, 0),
    }

    ICON_PATHS = {
        'house': './assets/resources/houses/house1.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
        'upgrade': './assets/resources/icons/upgrade.png',
        'remove': './assets/resources/icons/remove.png',
    }

    COSTS = {
        'house': 1000,
        'road': 50,
        'energy': 2000,
    }

    BUILDING_IMAGES = {
        'house': './assets/resources/houses/house1.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
    }

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
        self.house_menu_visible = False
        self.occupied_cells = set()

        self.house_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['house']), (80, 80))
        self.road_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80))
        self.energy_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['energy']), (80, 80))

    def draw(self):
        self.grid.draw_grid()
        self.draw_selected_cell_outline()
        self.draw_game_elements()
        self.draw_houses_level()

    def draw_selected_cell_outline(self):
        if self.selected_cell:
            pygame.draw.rect(self.window, self.COLORS['white'],
                             (self.selected_cell[0], self.selected_cell[1], self.grid_size, self.grid_size), 2)
            if self.house_menu_visible:
                self.draw_house_menu()

    def draw_game_elements(self):
        if self.menu_bar_visible:
            self.draw_menu_bar()
            if self.selected_cell:
                pygame.draw.rect(self.window, self.COLORS['yellow'],
                                 (self.selected_cell[0], self.selected_cell[1], self.grid_size, self.grid_size), 2)

        if self.game_state.climateScore <= 0:
            self.draw_game_over()
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    def draw_menu_bar(self):
        pygame.draw.rect(self.window, self.COLORS['menu_background'], (0, self.height - 80, self.width, 80))
        self.draw_building_icons()
        self.draw_building_costs()

    def draw_building_icons(self):
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['house']), (80, 80)),
                         (10, self.height - 75))
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80)),
                         (100, self.height - 75))
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['energy']), (80, 80)),
                         (190, self.height - 80))

    def draw_building_costs(self):
        font = pygame.font.Font(None, 24)
        for i, building_type in enumerate(['house', 'road', 'energy']):
            cost_text = font.render(f"${self.COSTS[building_type]}", True, self.COLORS['white'])
            self.window.blit(cost_text, (60 + i * 90, self.height - 70))

    def draw_houses_level(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House):
                level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                self.window.blit(level_text, (obj.x, obj.y))


    def handle_click(self, x, y):
        # Convert the mouse click coordinates to grid coordinates
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size

        # Convert grid coordinates back to pixel coordinates
        pixel_x = grid_x * self.grid_size
        pixel_y = grid_y * self.grid_size

        # Check if a house, road or energy building already exists at the clicked cell
        for obj in self.game_state.placed_objects:
            if (isinstance(obj, House) or isinstance(obj, Road) or isinstance(obj, Energy)) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                # If a house, road or energy building exists, store its coordinates in self.selected_cell
                self.selected_cell = (pixel_x, pixel_y)
                self.house_menu_visible = True
                return

        if self.house_menu_visible:
            # If the house menu is visible, check if the upgrade or remove button was clicked
            if self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30:
                if self.selected_cell[0] -50 <= x <= self.selected_cell[0] + 40:
                    # Upgrade button was clicked
                    for obj in self.game_state.placed_objects:
                        if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                            # If the player has enough money, upgrade the house
                            if self.game_state.money >= obj.upgrade_cost and obj.level < 7:
                                obj.upgrade()
                                new_image = pygame.image.load(f'./assets/resources/houses/house{obj.level}.png')  # Upgrade the house image
                                obj.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
                                self.game_state.remove_money(obj.upgrade_cost)  # Deduct the cost of the upgrade
                                additional_inhabitants = random.randint(3, 8)
                                self.game_state.add_citizen(additional_inhabitants)  
                                obj.inhabitants += additional_inhabitants  
                            break
            if self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30:
                if self.selected_cell[0] + 50 <= x <= self.selected_cell[0] + 90:
                    # Remove button was clicked
                    for obj in self.game_state.placed_objects:
                        if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                            # Remove the house
                            self.game_state.placed_objects.remove(obj)
                            self.game_state.remove_citizen(obj.inhabitants)  # Remove the inhabitants of the house
                            self.game_state.remove_house(1)
                            break
            self.house_menu_visible = False
            self.selected_cell = None  # Clear the selected cell
        elif self.menu_bar_visible:
            # If the menu bar is visible, check if the house or road image was clicked
            if self.height - 80 <= y <= self.height - 10:
                if 10 <= x <= 90:
                    # House image was clicked
                    if self.selected_cell is not None:
                        # Check if a house already exists at the selected cell
                        for obj in self.game_state.placed_objects:
                            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                                # If a house exists, show the house menu
                                self.menu_bar_visible = False
                                self.house_menu_visible = True
                                break
                        else:
                            # If no house exists and the player has enough money, place a new house
                            if self.game_state.money >= 1000:
                                house = House(self.selected_cell[0], self.selected_cell[1], self.grid_size)
                                self.game_state.placed_objects.append(house)
                                self.game_state.remove_money(1000)
                                add_citizen = random.randint(3, 6)
                                self.game_state.add_citizen(add_citizen)
                                house.add_inhabitant(add_citizen)
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
                elif 190 <= x <= 270:
                    # Energy building image was clicked
                    if self.selected_cell is not None and self.game_state.money >= 2000:
                        energy = Energy(self.selected_cell[0], self.selected_cell[1], self.grid_size)
                        self.game_state.placed_objects.append(energy)
                        self.game_state.remove_money(2000)
                        self.game_state.add_climate_score(10)
                        self.selected_cell = None
                    self.menu_bar_visible = False
            else:
                # If the click was outside the menu bar, close the menu
                self.menu_bar_visible = False
                self.selected_cell = None  # Clear the selected cell
        else:
            # If the menu bar is not visible, show it and store the selected cell
            self.menu_bar_visible = True
            self.selected_cell = (pixel_x, pixel_y)

    def draw_house_menu(self):
        upgrade_cost = 0
        # Load the icons
        upgrade_icon = pygame.image.load('./assets/resources/icons/upgrade.png')
        remove_icon = pygame.image.load('./assets/resources/icons/remove.png')

        # Resize the icons
        icon_width = 30
        icon_height = 30
        upgrade_icon = pygame.transform.scale(upgrade_icon, (icon_width, icon_height))
        remove_icon = pygame.transform.scale(remove_icon, (icon_width, icon_height))

        # Calculate the position of the menu
        menu_x = self.selected_cell[0] - 80 + self.grid_size // 2  # Center the menu below the house
        menu_y = self.selected_cell[1] + self.grid_size

        # Draw the house menu background
        pygame.draw.rect(self.window, (230, 230, 230), (menu_x, menu_y, 160, 50))  # Lower the height of the menu

        # Draw the upgrade and remove buttons
        font = pygame.font.Font(None, 24)  # Create a font object

        # Get the upgrade cost and format it
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                upgrade_cost = obj.upgrade_cost
                break

        # Format the upgrade cost string
        if upgrade_cost >= 1000000000:
            upgrade_cost_str = f"${upgrade_cost / 1000000000}b"
        elif upgrade_cost >= 1000000:
            upgrade_cost_str = f"${upgrade_cost / 1000000}m"
        elif upgrade_cost >= 1000:
            upgrade_cost_str = f"${upgrade_cost / 1000}k"
        else:
            upgrade_cost_str = f"${upgrade_cost}"

        upgrade_text = font.render(upgrade_cost_str, True, (0, 0, 0))  # Create a Surface with the upgrade text
        self.window.blit(upgrade_icon, (menu_x + 10, menu_y + 10))  # Draw the upgrade icon
        self.window.blit(upgrade_text, (menu_x + 40, menu_y + 16))  # Draw the upgrade text
        self.window.blit(remove_icon, (menu_x + 110, menu_y + 10))  # Draw the remove icon

    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, self.COLORS['game_over_text'])
        text2 = font2.render('You have destroyed the climate!', 1, self.COLORS['game_over_text'])
        self.window.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
        self.window.blit(text2, (self.width // 2 - text2.get_width() // 2, self.height // 2 + text.get_height() // 2))