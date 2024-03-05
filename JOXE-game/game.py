from grid import Grid
from gamestate import Gamestate
from house import House
from road import Road
from energy import Energy
from tree import Tree
from resolution import Resolution
# from car import Car
from store import Store
import pygame
from trivia import Trivia
from pygame import mixer
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
        'store': './assets/resources/buildings/stores/store.png',
    }

    COSTS = {
        'house': 1000,
        'road': 50,
        'energy': 2000,
        'store': 3000,
        'tree': 250,
    }

    BUILDING_IMAGES = {
        'house': './assets/resources/houses/house1.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
        'tree': './assets/resources/nature/tree1.png',
        'store': './assets/resources/buildings/stores/store.png'
    }

    ECO_SCORE_BONUS = {
        'tree': 5,
        'store': -5
    }

    def __init__(self, window, width, height, grid_size, gamestate=None):
        self.res = Resolution()
        self.window = window
        self.width = self.res.width
        self.height = self.res.height
        self.grid_size = grid_size
        self.game_state = Gamestate()
        # self.car = Car(grid_size, self.game_state.placed_objects)
        self.font = pygame.font.Font(None, 36)
        self.grid = Grid(window, grid_size, self.game_state, self.font)
        self.selected_cell = None
        self.menu_bar_visible = False
        self.clicked_menu_visible = False
        self.road_placement_in_progress = False
        self.road_start_position = (0, 0)
        self.occupied_cells = set()
        self.averagestatfont = pygame.font.Font(None, 16)
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.total_elapsed_time = 0  # Total elapsed time in milliseconds
        self.current_date = datetime.datetime(2022, 1, 1)  # Start at January 1, 2022
        self.placing_house_sound = mixer.Sound('Sounds/Placing house SFX.mp3')

        self.house_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['house']), (80, 80))
        self.road_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80))
        self.energy_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['energy']), (80, 80))
        self.store_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['store']), (80, 80))

    # Methods to draw the game

    def draw(self):
        self.grid.draw_grid()
        self.draw_selected_cell_outline()
        self.draw_game_elements()
        self.draw_object_level()
        self.draw_date()
        # self.car.update()
        # self.car.draw(self.window)
        pygame.display.update()

    def draw_date(self):
        # Draw the current date on the screen
        text = self.font.render(self.current_date.strftime("%d/%m/%Y"), True, (255, 255, 255))
        self.window.blit(text, (self.width / 10 * 9, 0))  # Adjust the position as needed

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
            if self.clicked_menu_visible:
                self.draw_building_clicked_menu()

    def draw_game_elements(self):
        if self.menu_bar_visible:
            self.draw_menu_bar()
            if self.selected_cell:
                pygame.draw.rect(self.window, self.COLORS['yellow'],
                                 (self.selected_cell[0], self.selected_cell[1], self.grid_size, self.grid_size), 2)
        # GAME OVER
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
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['store']), (80, 80)),
                        (280, self.height - 75))
        self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['tree']), (80, 80)),
                        (370, self.height - 75))
        #BUILDING

    def draw_building_costs(self):
        font = pygame.font.Font(None, 24)
        for i, building_type in enumerate(['house', 'road', 'energy', 'store', 'tree']): #BUILDING
            cost_text = font.render(f"${self.COSTS.get(building_type, 0)}", True, self.COLORS['white'])
            self.window.blit(cost_text, (60 + i * 90, self.height - 70))

    def draw_object_level(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House):
                level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                self.window.blit(level_text, (obj.x, obj.y))
            elif isinstance(obj, Store):
                level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                self.window.blit(level_text, (obj.x, obj.y))

    # Handle methods
    def handle_click(self, x, y):
        grid_x, grid_y = self.get_grid_coordinates(x, y)

        if self.road_placement_in_progress:
            self.handle_road_placement(x, y)
            return
        if self.clicked_menu_visible:
            self.handle_clicked_menu_click(x, y)
            return
        if self.menu_bar_visible:
            self.handle_menu_bar_click(x, y)
            return
        if self.is_building_already_present(grid_x, grid_y):
            self.selected_cell = (grid_x * self.grid_size, grid_y * self.grid_size)
            self.clicked_menu_visible = True
            return
        
        self.menu_bar_visible = True
        self.selected_cell = (grid_x * self.grid_size, grid_y * self.grid_size)
        print(f"Clicked on cell ({grid_x}, {grid_y})")

    def handle_clicked_menu_click(self, x, y):
        if self.is_upgrade_button_clicked(x, y):
            self.handle_upgrade_button_click()
        elif self.is_remove_button_clicked(x, y):
            self.handle_remove_button_click()
        self.clicked_menu_visible = False
        self.selected_cell = None

    def get_grid_coordinates(self, x, y):
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size
        return grid_x, grid_y

    # IS BUILDING PRESENT BUT ONLY HOUSE GETS CHECKED
    def is_building_already_present(self, grid_x, grid_y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Store) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Road) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
        return False

    # Is button clicked methods
    def is_upgrade_button_clicked(self, x, y):
        return self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30 and \
            self.selected_cell[0] - 50 <= x <= self.selected_cell[0] + 40

    def is_remove_button_clicked(self, x, y):
        return self.selected_cell[1] + self.grid_size <= y <= self.selected_cell[1] + self.grid_size + 30 and \
            self.selected_cell[0] + 50 <= x <= self.selected_cell[0] + 90
    
    def is_house_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 10 <= x <= 90

    def is_road_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 100 <= x <= 180

    def is_energy_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 190 <= x <= 270
    
    def is_store_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 280 <= x <= 360
    
    def is_tree_icon_clicked(self, x, y):
        return self.height - 80 <= y <= self.height - 10 and 370 <= x <= 450 

    #ALSO ONLY CHECKS HOUSE
    def handle_upgrade_button_click(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 100:  # Check if money after upgrade is >= 0
                    self.game_state.remove_money(obj.upgrade_cost)  # Deduct money before upgrading
                    obj.upgrade()
                    self.upgrade_house(obj)
            elif isinstance(obj, Store) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 10:
                    self.game_state.remove_money(obj.upgrade_cost)
                    obj.upgrade()
                    self.upgrade_store(obj)
                else:
                    print("Not enough money to upgrade the house.")
                break

    def upgrade_house(self, house):
        new_image = pygame.image.load(f'./assets/resources/houses/house{house.level}.png')
        house.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        additional_inhabitants = random.randint(3, 8)
        self.game_state.add_citizen(additional_inhabitants)
        house.inhabitants += additional_inhabitants

    def upgrade_store(self, store):
        new_image = pygame.image.load(f'./assets/resources/buildings/stores/store{store.level}.png')
        store.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    #also only checks house
    def handle_remove_button_click(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                self.remove_house(obj)
                break
            elif isinstance(obj, Store) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                self.remove_store(obj)
                break
            elif isinstance(obj, Road) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                self.remove_road(obj)
                break

    def remove_house(self, house):
        self.game_state.placed_objects.remove(house)
        self.game_state.remove_citizen(house.inhabitants)
        self.game_state.remove_house(1)

    def remove_store(self, store):
        self.game_state.placed_objects.remove(store)

    def remove_road(self, road):
        self.game_state.placed_objects.remove(road)
        self.occupied_cells.remove((road.x, road.y))

    def handle_menu_bar_click(self, x, y):
        if self.is_house_icon_clicked(x, y):
            self.handle_house_icon_click()
        elif self.is_road_icon_clicked(x, y):
            self.handle_road_icon_click()
        elif self.is_energy_icon_clicked(x, y):
            self.handle_energy_icon_click()
        elif self.is_tree_icon_clicked(x, y):
            self.handle_tree_icon_click()  
        elif self.is_store_icon_clicked(x, y):  
            self.handle_store_icon_click()      
        else:
            self.menu_bar_visible = False
            self.selected_cell = None

    def handle_store_icon_click(self):
        if self.selected_cell is not None:
            for obj in self.game_state.placed_objects:
                if isinstance(obj, Store) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                    self.menu_bar_visible = False
                    self.store_menu_visible = True
                    break
            else:
                if self.game_state.money >= self.COSTS['store']:
                    self.place_new_store()
                self.selected_cell = None
            self.menu_bar_visible = False

    def place_new_store(self):
        if self.game_state.money >= self.COSTS['store']:
            store = Store(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(store)
            self.game_state.remove_money(self.COSTS['store'])
            self.game_state.add_climate_score(self.ECO_SCORE_BONUS['store'])
        else:
            print("Not enough money to place a new store.")

    def handle_tree_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['tree']:
            tree = Tree(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(tree)
            self.game_state.remove_money(self.COSTS['tree'])
            self.game_state.add_climate_score(self.ECO_SCORE_BONUS['tree']) 
            self.selected_cell = None

            # Display trivia popup
            trivia = Trivia(self.window)
            trivia.show_trivia()        

        else:
            print("Not enough money to place a tree.")
        self.menu_bar_visible = False

    def handle_house_icon_click(self):
        if self.selected_cell is not None:
            for obj in self.game_state.placed_objects:
                if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                    self.menu_bar_visible = False
                    self.clicked_menu_visible = True
                    break
            else:
                if self.game_state.money >= 1000:
                    self.place_new_house()
                self.selected_cell = None
            self.menu_bar_visible = False

    def place_new_house(self):
        # Play the placing house sound
        self.placing_house_sound.play()

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
            
    def get_cell_at_location(self, x, y):
        for obj in self.grid.get_all_cells():
            if obj.x == x and obj.y == y:
                return obj
        return None

    def handle_road_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= 50:
            # Set road placement in progress and store the starting position
            self.road_placement_in_progress = True
            self.road_start_position = self.selected_cell
            self.menu_bar_visible = False
        else:
            print("Not enough money to place a road.")

    def update_road_images(self):
        for cell in self.grid.get_all_cells():
            if cell.type in ['road', 'v-road', '+-road', 'cornerroad', 't-road']:
                x, y = cell.x, cell.y
                neighbors = [(x, y - self.grid_size), (x, y + self.grid_size), 
                            (x - self.grid_size, y), (x + self.grid_size, y)]
                horizontal_neighbors = 0
                vertical_neighbors = 0
                for nx, ny in neighbors:
                    neighbor = self.get_cell_at_location(nx, ny)
                    if neighbor is not None and neighbor.type in ['road', 'v-road', '+-road', 'cornerroad', 't-road' ]: 
                        if nx != x:  # Horizontal road
                            horizontal_neighbors += 1
                        if ny != y:  # Vertical road
                            vertical_neighbors += 1
                if horizontal_neighbors == 2 and vertical_neighbors == 1 or horizontal_neighbors == 1 and vertical_neighbors == 2:
                    cell.set_type('t-road')
                    if self.get_cell_at_location(x, y + self.grid_size) is None:  # No cell at the top
                        cell.image = pygame.transform.rotate(cell.image, 180)
                    elif self.get_cell_at_location(x, y - self.grid_size) is None:  # No cell at the bottom
                        cell.image = pygame.transform.rotate(cell.image, 0)
                    elif self.get_cell_at_location(x - self.grid_size, y) is None:  # No cell at the left
                        cell.image = pygame.transform.rotate(cell.image, 90)
                    elif self.get_cell_at_location(x + self.grid_size, y) is None:  # No cell at the right
                        cell.image = pygame.transform.rotate(cell.image, 270)
                elif horizontal_neighbors == 2 and vertical_neighbors == 2:
                    cell.set_type('+-road')
                elif vertical_neighbors == 2 or vertical_neighbors == 1 and horizontal_neighbors == 0:
                    cell.set_type('v-road')
                elif horizontal_neighbors == 2 or horizontal_neighbors == 1 and vertical_neighbors == 0:
                    cell.set_type('road')
                elif horizontal_neighbors == 1 and vertical_neighbors == 1:
                    cell.set_type('cornerroad')
                    if self.get_cell_at_location(x, y - self.grid_size) is not None and self.get_cell_at_location(x + self.grid_size, y) is not None:
                        cell.image = pygame.transform.rotate(cell.image, 90)  # Rotate 90 degrees
                    elif self.get_cell_at_location(x, y + self.grid_size) is not None and self.get_cell_at_location(x + self.grid_size, y) is not None:
                        cell.image = pygame.transform.rotate(cell.image, 0)  # Rotate 0 degrees
                    elif self.get_cell_at_location(x, y + self.grid_size) is not None and self.get_cell_at_location(x - self.grid_size, y) is not None:
                        cell.image = pygame.transform.rotate(cell.image, 270)  # Rotate 270 degrees
                    elif self.get_cell_at_location(x, y - self.grid_size) is not None and self.get_cell_at_location(x - self.grid_size, y) is not None:
                        cell.image = pygame.transform.rotate(cell.image, 180)  # Rotate 180 degrees


    def handle_road_placement(self, x, y):
        if self.game_state.money >= 50:
            start_x, start_y = self.road_start_position
            road_length_x = (x - start_x) // self.grid_size
            road_length_y = (y - start_y) // self.grid_size

            # Determine direction for road placement
            x_direction = 1 if road_length_x >= 0 else -1
            y_direction = 1 if road_length_y >= 0 else -1

            # Handle roads in x direction
            for i in range(abs(road_length_x) + 1):
                new_x = start_x + i * self.grid_size * x_direction
                new_y = start_y
                self.place_road_at_location(new_x, new_y)

            # Handle roads in y direction
            for i in range(abs(road_length_y) + 1):
                new_x = start_x
                new_y = start_y + i * self.grid_size * y_direction
                self.place_road_at_location(new_x, new_y)

            # Update the road images
            self.update_road_images()

            self.selected_cell = None
            self.road_placement_in_progress = False
            self.game_state.remove_money(50)
        else:
            print("Not enough money to place a road.")

    def place_road_at_location(self, x, y):
        # Check if a road is already present at the target grid cell
        if self.is_building_already_present(x // self.grid_size, y // self.grid_size):
            return None
            
        x = x + 60
        y = y + 60

        road = Road(x, y, self.grid_size)
        road.set_type('road')
        self.game_state.placed_objects.append(road)
        self.game_state.remove_money(50)
        self.game_state.remove_climate_score(1)
        self.occupied_cells.add((x, y))

        # Check for nearby roads to connect
        self.connect_nearby_roads(x, y)

        # Return the road object
        return road
 
    def connect_nearby_roads(self, x, y):
        nearby_cells = [
            (x - self.grid_size, y),
            (x + self.grid_size, y),
            (x, y - self.grid_size),
            (x, y + self.grid_size),
        ]
        for cell in nearby_cells:
            cell_x, cell_y = cell
            if (cell_x, cell_y) in self.occupied_cells:
                self.update_adjacent_roads(cell_x, cell_y, nearby_cells)

    def update_adjacent_roads(self, x, y, nearby_cells):
        for cell in nearby_cells:
            cell_x, cell_y = cell
            for obj in self.game_state.placed_objects:
                if isinstance(obj, Road) and obj.x == cell_x and obj.y == cell_y:
                    self.check_adjacent_roads(x, y, cell_x, cell_y)
                    return

        # No nearby roads, use default horizontal road image
        self.set_road_image(x, y, 'road.png')

    def set_road_image(self, x, y, image_path):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Road) and obj.x == x and obj.y == y:
                print(f"Setting road image at ({x}, {y}) to {image_path}")
                if image_path == 'v-road.png' or image_path == 'cornerroad.png':
                    new_image = pygame.image.load(image_path)
                else:
                    # Load the original image
                    original_image = pygame.image.load(image_path)
                    # Create a new surface with the desired size
                    new_image = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
                    # Blit the original image onto the new surface
                    new_image.blit(original_image, (0, 0))
                obj.image = new_image

    def check_adjacent_roads(self, x1, y1, x2, y2):
        if x1 == x2:  # Same column
            for obj in self.game_state.placed_objects:
                if isinstance(obj, Road):
                    if obj.x == x1 and obj.y == y1:
                        self.set_road_image(x1, y1, 'v-road.png')
                    elif obj.x == x2 and obj.y == y2:
                        self.set_road_image(x2, y2, 'v-road.png')
        elif y1 == y2:  # Same row
            for obj in self.game_state.placed_objects:
                if isinstance(obj, Road):
                    if obj.x == x1 and obj.y == y1:
                        self.set_road_image(x1, y1, 'road.png')
                    elif obj.x == x2 and obj.y == y2:
                        self.set_road_image(x2, y2, 'road.png')
        else:  # Corner road
            self.set_road_image(x1, y1, 'cornerroad.png')
            self.set_road_image(x2, y2, 'cornerroad.png')

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

    def draw_building_clicked_menu(self):
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

        # Get the upgrade cost
        upgrade_cost = self.get_upgrade_cost(House)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Store)

    # Check if upgrade_cost is not None before comparing it with an integer
        if upgrade_cost is not None and upgrade_cost >= 1000000000:
            upgrade_cost_text = f'{upgrade_cost / 1000000000:.2f}B'
        elif upgrade_cost is not None and upgrade_cost >= 1000000:
            upgrade_cost_text = f'{upgrade_cost / 1000000:.2f}M'
        elif upgrade_cost is not None and upgrade_cost >= 1000:
            upgrade_cost_text = f'{upgrade_cost / 1000:.2f}K'
        else:
            upgrade_cost_text = str(upgrade_cost)

        upgrade_text = font.render(upgrade_cost_text, True, (0, 0, 0))  # Create a Surface with the upgrade text
        self.window.blit(upgrade_icon, (menu_x + 10, menu_y + 10))  # Draw the upgrade icon
        self.window.blit(upgrade_text, (menu_x + 40, menu_y + 16))  # Draw the upgrade text
        self.window.blit(remove_icon, (menu_x + 110, menu_y + 10))  # Draw the remove icon

    def draw_building_clicked_menu_remove_only(self):
        # Load the remove icon
        remove_icon = pygame.image.load('./assets/resources/icons/remove.png')

        # Resize the icon
        icon_width = 30
        icon_height = 30
        remove_icon = pygame.transform.scale(remove_icon, (icon_width, icon_height))

        # Calculate the position of the menu
        menu_x = self.selected_cell[0] - 80 + self.grid_size // 2
        menu_y = self.selected_cell[1] + self.grid_size

        # Draw the menu background
        pygame.draw.rect(self.window, (230, 230, 230), (menu_x, menu_y, 160, 50))

        # Draw the remove button
        self.window.blit(remove_icon, (menu_x + 110, menu_y + 10))


    def get_upgrade_cost(self, object_type):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, object_type) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                return obj.upgrade_cost
        return None

    # def print_game_grid(self):
    #     print("---------------------------------")
    #     grid_representation = [['.' for _ in range(self.width // self.grid_size)] for _ in range(self.height // self.grid_size)]

    #     for obj in self.game_state.placed_objects:
    #         x, y = obj.x // self.grid_size, obj.y // self.grid_size
    #         if isinstance(obj, House):
    #             grid_representation[y][x] = 'H'
    #         elif isinstance(obj, Road):
    #             grid_representation[y][x] = 'R'
    #         elif isinstance(obj, Tree):
    #             grid_representation[y][x] = 'T'
    #         elif isinstance(obj, Store):
    #             grid_representation[y][x] = 'S'
    #         elif isinstance(obj, Energy):
    #             grid_representation[y][x] = 'W'

    #     for row in grid_representation:
    #         print(" ".join(row))

    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, self.COLORS['game_over_text'])
        text2 = font2.render('You have destroyed the climate!', 1, self.COLORS['game_over_text'])
        self.window.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
        self.window.blit(text2, (self.width // 2 - text2.get_width() // 2, self.height // 2 + text.get_height() // 2))

    # def print_roads(self):
    #     for row in range(self.height // self.grid_size):
    #         for col in range(self.width // self.grid_size):
    #             road_present = any(
    #                 isinstance(obj, Road) and obj.x // self.grid_size == col and obj.y // self.grid_size == row
    #                 for obj in self.game_state.placed_objects
    #             )
    #             print("R" if road_present else ".", end=" ")
    #         print()