from grid import Grid
from gamestate import Gamestate
from house import House
from road import Road
from energy import Energy
from tree import Tree
import pygame
import os
import sys
import random
import datetime

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
        'tree': 250,
    }

    BUILDING_IMAGES = {
        'house': './assets/resources/houses/house1.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
        'tree': './assets/resources/nature/tree1.png',
    }

    ECO_SCORE_BONUS = {
    'tree': 5,
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
        self.font = pygame.font.Font(None, 36)
        self.averagestatfont = pygame.font.Font(None, 16)
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.total_elapsed_time = 0  # Total elapsed time in milliseconds
        self.current_date = datetime.datetime(2022, 1, 1)  # Start at January 1, 2022

        self.house_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['house']), (80, 80))
        self.road_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80))
        self.energy_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['energy']), (80, 80))

    def draw(self):
        self.grid.draw_grid()
        self.draw_selected_cell_outline()
        self.draw_game_elements()
        self.draw_houses_level()
        self.draw_date()

    def draw_date(self):
        # Draw the current date on the screen
        font = pygame.font.SysFont(None, 36)
        text = font.render(self.current_date.strftime("%d/%m/%Y"), True, (255, 255, 255))
        self.window.blit(text, (0, 0))  # Adjust the position as needed

    def draw_averages(self, average_money_gain, average_ecoscore_change):
        square_width, square_height = 100, 30
        square_x = self.width - square_width
        square_y = self.height - square_height
        square_color = (255, 255, 255)  # white

        pygame.draw.rect(self.window, square_color, (square_x, square_y, square_width, square_height))

        formatted_money_gain = self.format_number(average_money_gain)
        formatted_ecoscore_change = self.format_number(average_ecoscore_change)

        money_text = self.averagestatfont.render(f"$/m:   {formatted_money_gain}", True, (0, 0, 0))
        ecoscore_text = self.averagestatfont.render(f"CO2/m: {formatted_ecoscore_change}", True, (0, 0, 0))

        self.window.blit(money_text, (square_x + 12, square_y + 7))
        self.window.blit(ecoscore_text, (square_x + 12, square_y + 17))

    def format_number(self, num):
        sign = "+" if num > 0 else ""
        if num >= 1000000:
            return f"{sign}{round(num / 1000000)}m"
        elif num >= 1000:
            return f"{sign}{round(num / 1000)}k"
        else:
            return f"{sign}{round(num)}"

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
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['tree']), (80, 80)),
                        (280, self.height - 75))

    def draw_building_costs(self):
        font = pygame.font.Font(None, 24)
        for i, building_type in enumerate(['house', 'road', 'energy', 'tree']):
            cost_text = font.render(f"${self.COSTS.get(building_type, 0)}", True, self.COLORS['white'])
            self.window.blit(cost_text, (60 + i * 90, self.height - 70))

    def draw_houses_level(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House):
                level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                self.window.blit(level_text, (obj.x, obj.y))


    def handle_click(self, x, y):
        grid_x, grid_y = self.get_grid_coordinates(x, y)

        if self.house_menu_visible:
            self.handle_house_menu_click(x, y)
            return

        if self.menu_bar_visible:
            self.handle_menu_bar_click(x, y)
            return

        if self.is_building_already_present(grid_x, grid_y):
            self.selected_cell = (grid_x * self.grid_size, grid_y * self.grid_size)
            self.house_menu_visible = True
            return

        self.menu_bar_visible = True
        self.selected_cell = (grid_x * self.grid_size, grid_y * self.grid_size)

    def get_grid_coordinates(self, x, y):
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size
        return grid_x, grid_y

    def is_building_already_present(self, grid_x, grid_y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
        return False

    def handle_house_menu_click(self, x, y):
        if self.is_upgrade_button_clicked(x, y):
            self.handle_upgrade_button_click()
        elif self.is_remove_button_clicked(x, y):
            self.handle_remove_button_click()
        self.house_menu_visible = False
        self.selected_cell = None

    def is_upgrade_button_clicked(self, x, y):
        return self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30 and \
            self.selected_cell[0] - 50 <= x <= self.selected_cell[0] + 40

    def is_remove_button_clicked(self, x, y):
        return self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30 and \
            self.selected_cell[0] + 50 <= x <= self.selected_cell[0] + 90

    def handle_upgrade_button_click(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 7:  # Check if money after upgrade is >= 0
                    self.game_state.remove_money(obj.upgrade_cost)  # Deduct money before upgrading
                    obj.upgrade()
                    self.upgrade_house(obj)
                else:
                    print("Not enough money to upgrade the house.")
                break

    def upgrade_house(self, house):
        new_image = pygame.image.load(f'./assets/resources/houses/house{house.level}.png')
        house.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        additional_inhabitants = random.randint(3, 8)
        self.game_state.add_citizen(additional_inhabitants)
        house.inhabitants += additional_inhabitants

    def handle_remove_button_click(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                self.remove_house(obj)
                break

    def remove_house(self, house):
        self.game_state.placed_objects.remove(house)
        self.game_state.remove_citizen(house.inhabitants)
        self.game_state.remove_house(1)

    def handle_menu_bar_click(self, x, y):
        if self.is_house_icon_clicked(x, y):
            self.handle_house_icon_click()
        elif self.is_road_icon_clicked(x, y):
            self.handle_road_icon_click()
        elif self.is_energy_icon_clicked(x, y):
            self.handle_energy_icon_click()
        elif self.is_tree_icon_clicked(x, y):
            self.handle_tree_icon_click()
        else:
            self.menu_bar_visible = False
            self.selected_cell = None

    def is_tree_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 280 <= x <= 360  # Adjust the x-coordinate range for the tree icon

    def handle_tree_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['tree']:
            tree = Tree(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(tree)
            self.game_state.remove_money(self.COSTS['tree'])
            self.game_state.add_climate_score(self.ECO_SCORE_BONUS['tree']) 
            self.selected_cell = None
        else:
            print("Not enough money to place a tree.")
        self.menu_bar_visible = False

    def is_house_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 10 <= x <= 90

    def is_road_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 100 <= x <= 180

    def is_energy_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 190 <= x <= 270

    def handle_house_icon_click(self):
        if self.selected_cell is not None:
            for obj in self.game_state.placed_objects:
                if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                    self.menu_bar_visible = False
                    self.house_menu_visible = True
                    break
            else:
                if self.game_state.money >= 1000:
                    self.place_new_house()
                self.selected_cell = None
            self.menu_bar_visible = False

    def place_new_house(self):
        if self.game_state.money >= 1000:
            house = House(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(house)
            self.game_state.remove_money(1000)
            add_citizen = random.randint(3, 6)
            self.game_state.add_citizen(add_citizen)
            house.add_inhabitant(add_citizen)
            self.game_state.add_house(1)
        else:
            print("Not enough money to place a new house.")

    def handle_road_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= 50:
            self.place_road(self.selected_cell[0], self.selected_cell[1])
            self.menu_bar_visible = False
        else:
            print("Not enough money to place a road.")

    def place_road(self, start_x, start_y):
        end_x, end_y = start_x, start_y
        dragging = True

        while dragging:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    end_x, end_y = pygame.mouse.get_pos()
                    end_x -= end_x % self.grid_size
                    end_y -= end_y % self.grid_size

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False

            self.draw()
            pygame.draw.line(self.window, self.COLORS['white'], (start_x, start_y), (end_x, end_y), 5)
            pygame.display.update()

        road_length = max(abs((end_x - start_x) // self.grid_size), abs((end_y - start_y) // self.grid_size))

        for i in range(road_length + 1):
            road = Road(start_x + i * self.grid_size, start_y, self.grid_size)
            self.game_state.placed_objects.append(road)
            self.game_state.remove_money(50)
            self.game_state.remove_climate_score(1)

        self.selected_cell = None

    def handle_energy_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= 2000:
            energy = Energy(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(energy)
            self.game_state.remove_money(2000)
            self.game_state.add_climate_score(10)
            self.selected_cell = None
        else:
            print("Not enough money to place an energy building.")
        self.menu_bar_visible = False

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