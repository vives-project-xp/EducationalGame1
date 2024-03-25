from grid import Grid
from house import House
from road import Road
from energy import Energy
from tree import Tree
from resolution import Resolution
from factory import Factory
from store import Store
from hospital import Hospital
import pygame
from trivia import Trivia
from pygame import mixer
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
        'store': './assets/resources/buildings/stores/store1.png',
        'factory': './assets/resources/buildings/factory/tempfac1.png',
        'hospital': './assets/resources/buildings/hospital/hospital1.png',
    }

    COSTS = {
        'house': 1000,
        'road': 50,
        'energy': 2000,
        'store': 3000,
        'tree': 250,
        'factory': 10000,
        'hospital': 15000,
    }

    BUILDING_IMAGES = {
        'house': './assets/resources/houses/house1.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
        'tree': './assets/resources/nature/tree1.png',
        'store': './assets/resources/buildings/stores/store1.png',
        'factory': './assets/resources/buildings/factory/tempfac1.png',
        'hospital': './assets/resources/buildings/hospital/hospital1.png',
    }

    ECO_SCORE_BONUS = {
        'tree': 5,
        'store': -5
    }

    def __init__(self, window, grid_size, gamestate=None):
        self.res = Resolution()
        self.window = window
        self.width = self.res.width
        self.height = self.res.height
        self.grid_size = grid_size
        self.game_state = gamestate
        self.font = pygame.font.Font(None, 36)
        self.grid = Grid(window, grid_size, self.game_state, self.font)
        self.selected_cell = None
        self.menu_bar_visible = False
        self.clicked_menu_visible = False
        self.road_placement_in_progress = False
        self.road_start_position = (0, 0)
        self.occupied_cells = set()
        self.averagestatfont = pygame.font.Font(None, 16)
        self.placing_house_sound = mixer.Sound('Sounds/Placing house SFX.mp3')
        self.last_upgrade_click = pygame.time.get_ticks()
        self.game_over_timer_duration = 3000 
        self.game_over_timer_start = None
        self.game_over_displayed = False
        self.asset_width = 0.042 * self.width
        self.asset_height = 0.075 * self.height
        self.game_over = False
        self.icon_size = int(self.window.get_height() * 0.2 * 0.8)
        self.icon_y = int(0.8 * self.window.get_height()) + int(self.window.get_height() * 0.2 * 0.1) 
        self.menu_bar_height = self.window.get_height() * 0.2
        self.icon_size = int(self.menu_bar_height * 0.8) 

        self.house_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['house']), (80, 80))
        self.road_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80))
        self.energy_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['energy']), (80, 80))
        self.store_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['store']), (80, 80))
        self.factory_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['factory']), (80, 80))
        self.tree_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['tree']), (80, 80))
        self.hospital_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['hospital']), (80, 80))

    def draw(self):
        self.grid.draw_grid()
        self.draw_selected_cell_outline()
        self.draw_game_elements()
        self.draw_object_level()
        self.update_image_size()
        pygame.display.update()

    def update_image_size(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House):
                obj.update_position(self.grid_size)
            elif isinstance(obj, Store):
                obj.update_position(self.grid_size)
            # elif isinstance(obj, Road):
            #     obj.update_position(self.grid_size)
            elif isinstance(obj, Factory):
                obj.update_position(self.grid_size)
            # elif isinstance(obj, Tree):
            #     obj.update_position(self.grid_size)
            elif isinstance(obj, Energy):
                obj.update_position(self.grid_size)
            elif isinstance(obj, Hospital):
                obj.update_position(self.grid_size)

    # Drawing averages menu at bottom right corner
    def draw_averages(self, average_money_gain, average_ecoscore_change):
        square_width, square_height = self.window.get_width() / 20 , self.window.get_height() / 20
        square_x = self.window.get_width() - square_width
        square_y = self.window.get_height() - square_height
        square_color = (255, 255, 255) # Todo: pixel background

        pygame.draw.rect(self.window, square_color, (square_x, square_y, square_width, square_height))

        formatted_money_gain = self.format_number(average_money_gain)
        formatted_ecoscore_change = self.format_number(average_ecoscore_change)

        font_size = max(int(square_height / 2.5), 10) 
        sizedfont = pygame.font.Font(None, font_size)

        money_text = sizedfont.render(f"$/m:   {formatted_money_gain}", True, (0, 0, 0))
        ecoscore_text = sizedfont.render(f"CO2/m: {formatted_ecoscore_change}", True, (0, 0, 0))

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
            
            if self.clicked_menu_visible and not self.is_road_in_cell(self.selected_cell[0] // self.grid_size, self.selected_cell[1] // self.grid_size):
                self.draw_building_clicked_menu()
            elif self.clicked_menu_visible and self.is_road_in_cell(self.selected_cell[0] // self.grid_size, self.selected_cell[1] // self.grid_size):
                self.draw_building_clicked_menu_remove_only()

    def draw_game_elements(self):
        if self.menu_bar_visible:
            self.draw_menu_bar()
            if self.selected_cell:
                pygame.draw.rect(self.window, self.COLORS['yellow'],
                                (self.selected_cell[0], self.selected_cell[1], self.grid_size, self.grid_size), 2)

        if self.game_state.climateScore <= 0:
            if not self.game_over_displayed:
                if self.game_over_timer_start is None:
                    self.game_over_timer_start = pygame.time.get_ticks()

                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.game_over_timer_start

                if elapsed_time >= self.game_over_timer_duration:
                    self.game_state.game_over = True
                    self.game_over_timer_start = None
            else:
                self.game_state.game_over = True

    def draw_menu_bar(self):
        menu_bar_y = int(0.8 * self.window.get_height())
        pygame.draw.rect(self.window, self.COLORS['menu_background'], (0, menu_bar_y, self.window.get_width(), self.menu_bar_height))
        self.draw_building_icons(menu_bar_y, self.menu_bar_height)
        self.draw_building_costs(menu_bar_y)

    def draw_building_icons(self, menu_bar_y, menu_bar_height):
        icon_y = menu_bar_y + int(menu_bar_height * 0.1)  # Centered in the menu bar
        for i, building_type in enumerate(['house', 'road', 'energy', 'store', 'tree', 'factory', 'hospital']): #BUILDING
            self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES[building_type]), (self.icon_size, self.icon_size)),
                             (10 + i * (self.icon_size + 10), icon_y))

    def draw_building_costs(self, menu_bar_y):
        font = pygame.font.Font(None, 24)
        for i, building_type in enumerate(['house', 'road', 'energy', 'store', 'tree', 'factory', 'hospital']): #BUILDING
            cost_text = font.render(f"${self.COSTS.get(building_type, 0)}", True, self.COLORS['white'])
            self.window.blit(cost_text, (10 + i * (self.icon_size + 10), menu_bar_y + 5))

    def draw_object_level(self):
        for obj in self.game_state.placed_objects:
            if self.selected_cell is not None:
                if isinstance(obj, House):
                    level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                    self.window.blit(level_text, (obj.x, obj.y))
                elif isinstance(obj, Store):
                    level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                    self.window.blit(level_text, (obj.x, obj.y))
                elif isinstance(obj, Factory):
                    level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                    self.window.blit(level_text, (obj.x, obj.y))
                elif isinstance(obj, Hospital):
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
        
        if not self.is_tree_in_cell(grid_x, grid_y):
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

    def is_building_already_present(self, grid_x, grid_y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Store) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Road) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Factory) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Hospital) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Tree) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
            elif isinstance(obj, Energy) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
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
        return self.icon_y - 80 <= y <= self.icon_y + self.icon_size and 10 <= x <= 10 + self.icon_size

    def is_road_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + self.icon_size + 10 <= x <= 10 + 2 * self.icon_size + 10

    def is_energy_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 2 * self.icon_size + 20 <= x <= 10 + 3 * self.icon_size + 20
    
    def is_store_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 3 * self.icon_size + 30 <= x <= 10 + 4 * self.icon_size + 30
    
    def is_tree_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 4 * self.icon_size + 40 <= x <= 10 + 5 * self.icon_size + 40
    
    def is_factory_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 5 * self.icon_size + 50 <= x <= 10 + 6 * self.icon_size + 50
    
    def is_hospital_icon_clicked(self, x, y):
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 7 * self.icon_size + 70 <= x <= 10 + 8 * self.icon_size + 70

    # Check if there's a tree in the cell
    def is_tree_in_cell(self, x, y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Tree) and obj.x == x * self.grid_size and obj.y == y * self.grid_size:
                return True
        return False
    
    def is_road_in_cell(self, x, y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Road) and obj.x == x * self.grid_size and obj.y == y * self.grid_size:
                return True
        return False

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
            elif isinstance(obj, Factory) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 10:
                    self.game_state.remove_money(obj.upgrade_cost)
                    obj.upgrade()
                    self.upgrade_factory(obj)
            elif isinstance(obj, Hospital) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 10:
                    self.game_state.remove_money(obj.upgrade_cost)
                    obj.upgrade()
                    self.upgrade_hospital(obj)
            elif isinstance(obj, Energy) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < 4:
                    self.game_state.remove_money(obj.upgrade_cost)
                    obj.upgrade()
                    self.upgrade_energy(obj)
                else:
                    print("Not enough money to upgrade the house.")
                break

    def upgrade_house(self, house):
        new_image = pygame.image.load(f'./assets/resources/houses/house{house.level}.png')
        house.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        additional_inhabitants = random.randint(house.level, house.level * 3)
        self.game_state.add_citizen(additional_inhabitants)
        house.inhabitants += additional_inhabitants

    def upgrade_store(self, store):
        new_image = pygame.image.load(f'./assets/resources/buildings/stores/store{store.level}.png')
        store.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    def upgrade_factory(self, factory):
        new_image = pygame.image.load(f'./assets/resources/buildings/factory/tempfac{factory.level}.png')
        factory.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    def upgrade_hospital(self, hospital):
        new_image = pygame.image.load(f'./assets/resources/buildings/hospital/hospital{hospital.level}.png')
        hospital.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    def upgrade_energy(self, windmill):
        new_image = pygame.image.load(f'./assets/resources/buildings/energy/windmills/windmill{windmill.level}.png')
        windmill.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    def handle_remove_button_click(self):
        # Print the coordinates of the selected cell
        print("Selected cell:", self.selected_cell)

        # Find the object at the selected cell
        selected_object = None
        for obj in self.game_state.placed_objects:
            # Print the coordinates of the object
            print("Object coordinates:", (obj.x, obj.y))
            if isinstance(obj, Road):
                obj.x == self.selected_cell[0] + 50 and obj.y == self.selected_cell[1] + 50
                print("selected cell2:", (obj.x, obj.y))
                selected_object = obj
            else:
                if obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                    selected_object = obj
                    break

        if selected_object is not None:
            if isinstance(selected_object, House):
                self.remove_house(selected_object)
            elif isinstance(selected_object, Store):
                self.remove_store(selected_object)
            elif isinstance(selected_object, Road):
                self.remove_road(selected_object)
            elif isinstance(selected_object, Factory):
                self.remove_factory(selected_object)
            elif isinstance(selected_object, Hospital):
                self.remove_hospital(selected_object)
            elif isinstance(selected_object, Tree):
                self.remove_tree(selected_object)
            elif isinstance(selected_object, Energy):
                self.remove_energy(selected_object)
        else:
            print("No object found at the selected cell.")


    def remove_house(self, house):
        self.game_state.placed_objects.remove(house)
        self.game_state.remove_citizen(house.inhabitants)
        self.game_state.remove_house(1)
        self.game_state.remove_citizen_happiness(3)

    def remove_store(self, store):
        self.game_state.placed_objects.remove(store)
        self.game_state.remove_citizen_happiness(5)

    def remove_tree(self, tree):
        self.game_state.placed_objects.remove(tree)
        self.game_state.remove_climate_score(2)

    def remove_road(self, road):
        self.game_state.placed_objects.remove(road)
        self.game_state.add_citizen_happiness(1)

    def remove_factory(self, factory):
        self.game_state.placed_objects.remove(factory)
        self.game_state.add_citizen_happiness(10)

    def remove_hospital(self, hospital):
        self.game_state.placed_objects.remove(hospital)
        self.game_state.remove_citizen_happiness(5)

    def remove_energy(self, energy):
        self.game_state.placed_objects.remove(energy)
        self.game_state.remove_climate_score(5)

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
        elif self.is_factory_icon_clicked(x, y):
            self.handle_factory_icon_click()  
        elif self.is_hospital_icon_clicked(x, y):
            self.handle_hospital_icon_click()
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
            self.game_state.add_citizen_happiness(5)
        else:
            print("Not enough money to place a new store.")

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
        
        # Display trivia popup with 40 percent spawn chance
        if random.randint(1, 100) <= 40:
            trivia = Trivia(self.window)
            trivia.show_trivia()   
        
    def handle_hospital_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['hospital']:
            hospital = Hospital(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(hospital)
            self.game_state.remove_money(self.COSTS['hospital'])
            self.selected_cell = None
        else:
            print("Not enough money to place a hospital.")
        self.menu_bar_visible = False

    def place_new_hospital(self):
        hospital = Hospital(self.selected_cell[0], self.selected_cell[1], self.grid_size)
        self.game_state.placed_objects.append(hospital)
        self.game_state.remove_money(self.COSTS['hospital'])
        self.game_state.add_climate_score(self.ECO_SCORE_BONUS['hospital'])
        self.game_state.add_citizen_happiness(5)
        self.selected_cell = None

    def handle_factory_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['factory']:
            factory = Factory(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(factory)
            self.game_state.remove_money(self.COSTS['factory'])
            self.selected_cell = None
            self.game_state.remove_citizen_happiness(25)
        else:
            print("Not enough money to place a factory.")
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
        self.placing_house_sound.play()

        if self.game_state.money >= 1000:
            house = House(self.selected_cell[0], self.selected_cell[1], self.grid_size) 
            self.game_state.placed_objects.append(house)
            self.game_state.remove_money(1000)
            add_citizen = random.randint(3, 6)
            self.game_state.add_citizen(add_citizen)
            house.add_inhabitant(add_citizen)
            self.game_state.add_house(1)
            self.game_state.add_citizen_happiness(1)
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
                        cell.set_rotation(180)
                    elif self.get_cell_at_location(x, y - self.grid_size) is None:  # No cell at the bottom
                        cell.set_rotation(0)
                    elif self.get_cell_at_location(x - self.grid_size, y) is None:  # No cell at the left
                        cell.set_rotation(90)
                    elif self.get_cell_at_location(x + self.grid_size, y) is None:  # No cell at the right
                        cell.set_rotation(270)
                    cell.update_image()
                elif horizontal_neighbors == 2 and vertical_neighbors == 2:
                    cell.set_type('+-road')
                elif vertical_neighbors == 2 or vertical_neighbors == 1 and horizontal_neighbors == 0:
                    cell.set_type('v-road')
                elif horizontal_neighbors == 2 or horizontal_neighbors == 1 and vertical_neighbors == 0:
                    cell.set_type('road')
                elif horizontal_neighbors == 1 and vertical_neighbors == 1:
                    cell.set_type('cornerroad')
                    if self.get_cell_at_location(x, y - self.grid_size) is not None and self.get_cell_at_location(x + self.grid_size, y) is not None:
                        cell.set_rotation(90)
                    elif self.get_cell_at_location(x, y + self.grid_size) is not None and self.get_cell_at_location(x + self.grid_size, y) is not None:
                        cell.set_rotation(0)
                    elif self.get_cell_at_location(x, y + self.grid_size) is not None and self.get_cell_at_location(x - self.grid_size, y) is not None:
                        cell.set_rotation(270)
                    elif self.get_cell_at_location(x, y - self.grid_size) is not None and self.get_cell_at_location(x - self.grid_size, y) is not None:
                        cell.set_rotation(180)
                    cell.update_image()

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
        for obj in self.game_state.placed_objects:
            print(obj.x, obj.y)
        self.game_state.remove_money(50)
        self.game_state.remove_climate_score(1)
        self.occupied_cells.add((x - 60, y - 60))

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

        # Draw the border of the menu
        border_width = 2  # You can change this to make the border thicker or thinner
        pygame.draw.rect(self.window, (0, 0, 0), (menu_x, menu_y, 160, 50), border_width)

        # Draw the upgrade and remove buttons
        font = pygame.font.Font(None, 24)  # Create a font object

        # Get the upgrade cost
        upgrade_cost = self.get_upgrade_cost(House)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Store)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Factory)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Hospital)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Energy)

        # Check if upgrade_cost is not None before comparing it with an integer
        if upgrade_cost is not None and upgrade_cost >= 1000000000:
            upgrade_cost_text = f'{upgrade_cost / 1000000000:.2f}B'
        elif upgrade_cost is not None and upgrade_cost >= 1000000:
            upgrade_cost_text = f'{upgrade_cost / 1000000:.2f}M'
        elif upgrade_cost is not None and upgrade_cost >= 1000:
            upgrade_cost_text = f'{upgrade_cost / 1000:.2f}K'
        else:
            upgrade_cost_text = str(upgrade_cost)

        text_color = (0, 0, 0)
        if upgrade_cost is not None:
            if self.game_state.money < upgrade_cost:
                text_color = (255, 0, 0)
            else:
                text_color = (0, 0, 0)

        upgrade_text = font.render(upgrade_cost_text, True, text_color)  # Create a Surface with the upgrade text
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

    def draw_game_over(self):
        font = pygame.font.Font(None, 170)
        font2 = pygame.font.Font(None, 50)
        text = font.render('Game Over', 1, self.COLORS['game_over_text'])
        text2 = font2.render('You have destroyed the climate!', 1, self.COLORS['game_over_text'])
        self.window.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
        self.window.blit(text2, (self.width // 2 - text2.get_width() // 2, self.height // 2 + text.get_height() // 2))
        #play again button
        pygame.draw.rect(self.window, self.COLORS['white'], (self.width // 2 - 100, self.height // 2 + 200, 200, 50))
        font3 = pygame.font.Font(None, 36)
        text3 = font3.render('Play Again', 1, self.COLORS['game_over_text'])
        self.window.blit(text3, (self.width // 2 - text3.get_width() // 2, self.height // 2 + 200 + 10))
        if self.width // 2 - 100 <= pygame.mouse.get_pos()[0] <= self.width // 2 + 100 and self.height // 2 + 200 <= pygame.mouse.get_pos()[1] <= self.height // 2 + 250:
            if pygame.mouse.get_pressed()[0]:
                self.game_state.game_over = False
                self.game_over = False
                self.game_state.restart()
                self.game_over_timer_start = None
                self.grid.update_date()

        #quit button
        pygame.draw.rect(self.window, self.COLORS['white'], (self.width // 2 - 100, self.height // 2 + 300, 200, 50))
        text4 = font3.render('Quit', 1, self.COLORS['game_over_text'])
        self.window.blit(text4, (self.width // 2 - text4.get_width() // 2, self.height // 2 + 300 + 10))
        if self.width // 2 - 100 <= pygame.mouse.get_pos()[0] <= self.width // 2 + 100 and self.height // 2 + 300 <= pygame.mouse.get_pos()[1] <= self.height // 2 + 350:
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()


