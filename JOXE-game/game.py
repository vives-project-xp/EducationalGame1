from grid import Grid
from zobjectfiles.house import House
from zobjectfiles.road import Road
from zobjectfiles.energy import Energy
from zobjectfiles.tree import Tree
from zobjectfiles.factory import Factory
from zobjectfiles.store import Store
from zobjectfiles.hospital import Hospital
from zobjectfiles.firestation import Firestation
from zobjectfiles.empty import Empty
from resolution import Resolution
from trivia import Trivia
import pygame, sys, random
from pygame import mixer
import sys
import random
import time

class Game:
    COLORS = {
        'white': (255, 255, 255),
        'yellow': (255, 255, 0),
        'red': (255, 0, 0),
        'menu_background': (230, 230, 230),
        'game_over_text': (255, 0, 0),
    }

    COSTS = {
        'house': 1000,
        'road': 50,
        'energy': 2000,
        'store': 3000,
        'tree': 250,
        'factory': 10000,
        'hospital': 15000,
        'firestation': 20000,
    }

    BUILDING_IMAGES = {
        'house': './assets/resources/houses/house11.png',
        'road': './assets/resources/road/road.png',
        'energy': './assets/resources/buildings/energy/windmills/windmill.png',
        'tree': './assets/resources/nature/tree/tree1.png',
        'store': './assets/resources/buildings/stores/store1.png',
        'factory': './assets/resources/buildings/factory/tempfac1.png',
        'hospital': './assets/resources/buildings/hospital/hospital1.png',
        'firestation': './assets/resources/buildings/firestation/firestation1.png',
    }

    ECO_SCORE_BONUS = {
        'tree': 5,
        'store': -5,
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
        self.placing_house_sound = mixer.Sound('Sounds/Placing house SFX.mp3')
        self.placesound = pygame.mixer.Sound('./Sounds/Place.mp3')
        self.game_over_timer_duration = 3000 
        self.game_over_timer_start = None
        self.game_over_displayed = False
        self.game_over = False
        self.icon_size = int(self.window.get_height() * 0.2 * 0.8)
        self.icon_y = int(0.8 * self.window.get_height()) + int(self.window.get_height() * 0.2 * 0.1) 
        self.menu_bar_height = self.window.get_height() * 0.2

        self.icon_size = int(self.menu_bar_height * 0.8) 
        self.warning_popup = False

        self.road_image = pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES['road']), (80, 80))

    def draw(self):
        self.grid.draw_grid()
        self.draw_selected_cell_outline()
        self.draw_game_elements()
        self.draw_object_level()
        self.update_image_size()
        self.update_effect_happiness()
        self.citizen_happiness_update()
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
            elif isinstance(obj, Tree):
                obj.update_position(self.grid_size)
            elif isinstance(obj, Energy):
                obj.update_position(self.grid_size)
            elif isinstance(obj, Hospital):
                obj.update_position(self.grid_size)
            elif isinstance(obj, Firestation):
                obj.update_position(self.grid_size)

    def draw_averages(self, average_money_gain, average_ecoscore_change):
        square_width, square_height = self.window.get_width() / 20 , self.window.get_height() / 20
        square_x = self.window.get_width() - square_width
        square_y = self.window.get_height() - square_height
        square_color = (255, 255, 255) 

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
            
            # Get the object in the selected cell
            obj_in_cell = self.get_object_in_cell(self.selected_cell[0] // self.grid_size, self.selected_cell[1] // self.grid_size)

            if self.clicked_menu_visible and not self.is_road_in_cell(self.selected_cell[0] // self.grid_size, self.selected_cell[1] // self.grid_size) and not isinstance(obj_in_cell, Empty):
                self.draw_building_clicked_menu()

    def get_object_in_cell(self, x, y):
        for obj in self.game_state.placed_objects:
            if obj.x == x * self.grid_size and obj.y == y * self.grid_size:
                return obj
        return None

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
        for i, building_type in enumerate(['house', 'road', 'energy', 'store', 'tree', 'factory', 'hospital', 'firestation']): #BUILDING
            self.window.blit(pygame.transform.scale(pygame.image.load(self.BUILDING_IMAGES[building_type]), (self.icon_size, self.icon_size)),
                             (10 + i * (self.icon_size + 10), icon_y))

    def draw_building_costs(self, menu_bar_y):
        font = pygame.font.Font(None, 24)
        for i, building_type in enumerate(['house', 'road', 'energy', 'store', 'tree', 'factory', 'hospital', 'firestation']): #BUILDING
            cost = self.COSTS.get(building_type, 0)
            if self.game_state.money < cost: 
                color = self.COLORS['red']
            else:
                color = self.COLORS['white'] 
            cost_text = font.render(f"${cost}", True, color)
            self.window.blit(cost_text, (10 + i * (self.icon_size + 10), menu_bar_y + 5))

    # If the player has not enough money to place a building, place a warning popup
    def draw_warning_popup(self):
        if self.warning_popup:
            if time.time() - self.last_upgrade_click > 3:
                self.warning_popup = False
            else:
                warning_text = self.font.render("Not enough money to place this building", True, self.COLORS['red'])
                self.window.blit(warning_text, (self.window.get_width() // 2 - 200, self.window.get_height() // 2))

         
    def draw_object_level(self):
        if self.selected_cell is not None:
            for obj in self.game_state.placed_objects:
                if isinstance(obj, (House, Store, Factory, Hospital, Energy, Tree, Firestation)):
                    level_text = self.font.render(str(obj.level), True, self.COLORS['white'])
                    self.window.blit(level_text, (obj.x, obj.y))

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
            if isinstance(obj, (House, Store, Road, Factory, Hospital, Tree, Energy, Firestation, Empty)) and obj.x // self.grid_size == grid_x and obj.y // self.grid_size == grid_y:
                return True
        return False

    def is_upgrade_button_clicked(self, x, y):
        menu_x, menu_y = self.get_menu_position()
        return menu_y <= y <= menu_y + 30 and \
            menu_x <= x <= menu_x + 80

    def is_remove_button_clicked(self, x, y):
        menu_x, menu_y = self.get_menu_position()
        return menu_y <= y <= menu_y + 30 and \
            menu_x + 100 <= x <= menu_x + 160
    
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
        return self.icon_y <= y <= self.icon_y + self.icon_size and 10 + 6 * self.icon_size + 60 <= x <= 10 + 7 * self.icon_size + 60

    def is_firestation_icon_clicked(self, x, y):
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
            if obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                max_level = 10 if isinstance(obj, (Store, Factory, Hospital, Firestation)) else 4 if isinstance(obj, (Energy, House)) else 3 if isinstance(obj, Tree) else 0
                # add new building here
                upgrade_method = self.upgrade_house if isinstance(obj, House) else self.upgrade_store if isinstance(obj, Store) else self.upgrade_factory if isinstance(obj, Factory) else self.upgrade_hospital if isinstance(obj, Hospital) else self.upgrade_energy if isinstance(obj, Energy) else self.upgrade_tree if isinstance(obj, Tree) else self.upgrade_firestation if isinstance(obj, Firestation) else None
                if isinstance(obj, Empty):
                    return
                else:
                    if self.game_state.money - obj.upgrade_cost >= 0 and obj.level < max_level:
                        pygame.mixer.init()
                        levelupsound = pygame.mixer.Sound('./Sounds/Levelup.mp3')
                        levelupsound.set_volume(0.5)
                        levelupsound.play()
                        self.game_state.remove_money(obj.upgrade_cost)
                        obj.upgrade()
                        upgrade_method(obj)
                    else:
                        print("Not enough money to upgrade the house.")
                    break

    def upgrade_house(self, house):
        new_image = pygame.image.load(f'./assets/resources/houses/house{house.version}{house.level}.png')
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
        factory.lower_effect_range(1)

    def upgrade_hospital(self, hospital):
        new_image = pygame.image.load(f'./assets/resources/buildings/hospital/hospital{hospital.level}.png')
        hospital.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        hospital.higher_effect_range(1)

    def upgrade_firestation(self, firestation):
        new_image = pygame.image.load(f'./assets/resources/buildings/firestation/firestation{firestation.level}.png')
        firestation.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        firestation.higher_effect_range(1)

    def upgrade_energy(self, windmill):
        new_image = pygame.image.load(f'./assets/resources/buildings/energy/windmills/windmill{windmill.level}.png')
        windmill.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))

    def upgrade_tree(self, tree):
        new_image = pygame.image.load(f'./assets/resources/nature/tree/tree{tree.level}.png')
        tree.image = pygame.transform.scale(new_image, (self.grid_size, self.grid_size))
        tree.higher_effect_range(1)

    def handle_remove_button_click(self):
        print("Selected cell:", self.selected_cell)

        selected_object = None
        for obj in self.game_state.placed_objects:
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
            if isinstance(selected_object, Empty):
                return
            else:
                remove_method = self.remove_house if isinstance(selected_object, House) else self.remove_store if isinstance(selected_object, Store) else self.remove_road if isinstance(selected_object, Road) else self.remove_factory if isinstance(selected_object, Factory) else self.remove_hospital if isinstance(selected_object, Hospital) else self.remove_tree if isinstance(selected_object, Tree) else self.remove_energy if isinstance(selected_object, Energy) else self.remove_firestation if isinstance(selected_object, Firestation) else None
                remove_method(selected_object)
        else:
            print("No object found at the selected cell.")

    def citizen_happiness_update(self):
        total_happiness = 0
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House):
                total_happiness += obj.inhab_happiness
        self.game_state.update_city_happiness(total_happiness)
        print("Total happiness:", total_happiness)

    def remove_house(self, house):
        self.game_state.placed_objects.remove(house)
        self.game_state.remove_citizen(house.inhabitants)
        self.game_state.remove_house(1)

    def remove_store(self, store):
        self.game_state.placed_objects.remove(store)

    def remove_tree(self, tree):
        self.remove_effect_happiness_tree(tree) 
        self.game_state.placed_objects.remove(tree)
        self.game_state.remove_climate_score(2)

    def remove_road(self, road):
        self.game_state.placed_objects.remove(road)

    def remove_factory(self, factory):
        self.remove_effect_happiness_factory(factory)
        self.game_state.placed_objects.remove(factory)

    def remove_hospital(self, hospital):
        self.remove_effect_happiness_hospital(hospital)
        self.game_state.placed_objects.remove(hospital)

    def remove_firestation(self, firestation):
        self.remove_effect_happiness_firestation(firestation)
        self.game_state.placed_objects.remove(firestation)

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
        elif self.is_firestation_icon_clicked(x, y):
            self.handle_firestation_icon_click()
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
            self.placesound.set_volume(0.5)
            self.placesound.play()
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
        else:
            print("Not enough money to place a tree.")
        self.menu_bar_visible = False
        
        # Display trivia popup with 40 percent spawn chance
        # if random.randint(1, 100) <= 40:
        trivia = Trivia(self.window, self.game_state)
        trivia.show_trivia()   
        self.placesound.set_volume(0.5)
        self.placesound.play()
        
    def handle_hospital_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['hospital']:
            self.place_new_hospital()
        else:
            print("Not enough money to place a hospital.")
        self.menu_bar_visible = False

    def place_new_hospital(self):
        hospital = Hospital(self.selected_cell[0], self.selected_cell[1], self.grid_size)
        self.game_state.placed_objects.append(hospital)
        self.placesound.set_volume(0.5)
        self.placesound.play()
        self.game_state.remove_money(self.COSTS['hospital'])
        self.game_state.remove_climate_score(5)
        self.selected_cell = None

    def handle_firestation_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['firestation']:
            self.place_new_firestation()
        else:
            print("Not enough money to place a firestation.")
        self.menu_bar_visible = False

    def place_new_firestation(self):
        firestation = Firestation(self.selected_cell[0], self.selected_cell[1], self.grid_size)
        self.game_state.placed_objects.append(firestation)
        self.placesound.set_volume(0.5)
        self.placesound.play()
        self.game_state.remove_money(self.COSTS['firestation'])
        self.game_state.remove_climate_score(5)
        self.selected_cell = None

    def update_effect_happiness(self):
        self.update_effect_happiness_hospital()
        self.update_effect_happiness_tree()
        self.update_effect_happiness_factory()

    def update_effect_happiness_hospital(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Hospital):
                effect_range = obj.effect_range
                for house in self.game_state.placed_objects:
                    if isinstance(house, House):
                        if obj.x - effect_range*self.res.GRID_SIZE <= house.x <= obj.x + effect_range*self.res.GRID_SIZE and obj.y - effect_range*self.res.GRID_SIZE <= house.y <= obj.y + effect_range*self.res.GRID_SIZE:
                            house.add_happiness(1)
                        print("House happiness:", house.inhab_happiness)

    def remove_effect_happiness_hospital(self, removed_hospital):
        effect_range = removed_hospital.effect_range
        for house in self.game_state.placed_objects:
            if isinstance(house, House):
                if removed_hospital.x - effect_range*self.res.GRID_SIZE <= house.x <= removed_hospital.x + effect_range*self.res.GRID_SIZE and removed_hospital.y - effect_range*self.res.GRID_SIZE <= house.y <= removed_hospital.y + effect_range*self.res.GRID_SIZE:
                    house.remove_happiness(1)
                print("House happiness:", house.inhab_happiness)

    def update_effect_happiness_tree(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Tree):
                effect_range = obj.effect_range
                for house in self.game_state.placed_objects:
                    if isinstance(house, House):
                        if obj.x - effect_range*self.res.GRID_SIZE <= house.x <= obj.x + effect_range*self.res.GRID_SIZE and obj.y - effect_range*self.res.GRID_SIZE <= house.y <= obj.y + effect_range*self.res.GRID_SIZE:
                            house.add_happiness(1)
                        print("House happiness:", house.inhab_happiness)

    def remove_effect_happiness_tree(self, removed_tree):
        effect_range = removed_tree.effect_range
        for house in self.game_state.placed_objects:
            if isinstance(house, House):
                if removed_tree.x - effect_range*self.res.GRID_SIZE <= house.x <= removed_tree.x + effect_range*self.res.GRID_SIZE and removed_tree.y - effect_range*self.res.GRID_SIZE <= house.y <= removed_tree.y + effect_range*self.res.GRID_SIZE:
                    house.remove_happiness(1)
                print("House happiness:", house.inhab_happiness)

    def update_effect_happiness_factory(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Factory):
                effect_range = obj.effect_range
                for house in self.game_state.placed_objects:
                    if isinstance(house, House):
                        if obj.x - effect_range*self.res.GRID_SIZE <= house.x <= obj.x + effect_range*self.res.GRID_SIZE and obj.y - effect_range*self.res.GRID_SIZE <= house.y <= obj.y + effect_range*self.res.GRID_SIZE:
                            house.remove_happiness(3)
                        print("House happiness:", house.inhab_happiness)

    def remove_effect_happiness_factory(self, removed_factory):
        effect_range = removed_factory.effect_range
        for house in self.game_state.placed_objects:
            if isinstance(house, House):
                if removed_factory.x - effect_range*self.res.GRID_SIZE <= house.x <= removed_factory.x + effect_range*self.res.GRID_SIZE and removed_factory.y - effect_range*self.res.GRID_SIZE <= house.y <= removed_factory.y + effect_range*self.res.GRID_SIZE:
                    house.add_happiness(3)
                print("House happiness:", house.inhab_happiness)

    def update_effect_happiness_firestation(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Firestation):
                effect_range = obj.effect_range
                for house in self.game_state.placed_objects:
                    if isinstance(house, House):
                        if obj.x - effect_range*self.res.GRID_SIZE <= house.x <= obj.x + effect_range*self.res.GRID_SIZE and obj.y - effect_range*self.res.GRID_SIZE <= house.y <= obj.y + effect_range*self.res.GRID_SIZE:
                            house.add_happiness(2)
                        print("House happiness:", house.inhab_happiness)

    def remove_effect_happiness_firestation(self, removed_firestation):
        effect_range = removed_firestation.effect_range
        for house in self.game_state.placed_objects:
            if isinstance(house, House):
                if removed_firestation.x - effect_range*self.res.GRID_SIZE <= house.x <= removed_firestation.x + effect_range*self.res.GRID_SIZE and removed_firestation.y - effect_range*self.res.GRID_SIZE <= house.y <= removed_firestation.y + effect_range*self.res.GRID_SIZE:
                    house.remove_happiness(2)
                print("House happiness:", house.inhab_happiness)

    def handle_factory_icon_click(self):
        if self.selected_cell is not None and self.game_state.money >= self.COSTS['factory']:
            factory = Factory(self.selected_cell[0], self.selected_cell[1], self.grid_size)
            self.game_state.placed_objects.append(factory)
            placesound = pygame.mixer.Sound('./Sounds/Place.mp3')
            placesound.set_volume(0.5)
            placesound.play()
            self.game_state.remove_money(self.COSTS['factory'])
            self.selected_cell = None
        else:
            self.draw_warning_popup()
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
                else: 
                    self.draw_warning_popup()
                    print("Not enough money to place a new house.")
                self.selected_cell = None
            self.menu_bar_visible = False

    def place_new_house(self):
        self.placing_house_sound.play()

        if self.game_state.money >= 1000:
            ran_version = random.randint(1, 4)
            house = House(self.selected_cell[0], self.selected_cell[1], self.grid_size, version=ran_version) 
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
            self.road_placement_in_progress = True
            self.road_start_position = self.selected_cell
            self.menu_bar_visible = False
        else:
            print("Not enough money to place a road.")

    def update_road_images(self):
        for cell in self.grid.get_all_cells():
            if cell.type in ['road', 'v-road', '+-road', 'cornerroad', 't-road', 'endroad']:
                x, y = cell.x, cell.y
                neighbors = [(x, y - self.grid_size), (x, y + self.grid_size), 
                            (x - self.grid_size, y), (x + self.grid_size, y)]
                neighbor_count = sum(1 for nx, ny in neighbors if self.get_cell_at_location(nx, ny) and self.get_cell_at_location(nx, ny).type in ['road', 'v-road', '+-road', 'cornerroad', 't-road', 'endroad'])
                if neighbor_count == 1:
                    cell.set_type('endroad')
                    if self.get_cell_at_location(x, y - self.grid_size):
                        cell.set_rotation(90)
                    elif self.get_cell_at_location(x, y + self.grid_size):
                        cell.set_rotation(270)
                    elif self.get_cell_at_location(x - self.grid_size, y):
                        cell.set_rotation(180)
                    elif self.get_cell_at_location(x + self.grid_size, y): 
                        cell.set_rotation(0)
                    cell.update_image()
                else:
                    horizontal_neighbors = 0
                    vertical_neighbors = 0
                    for nx, ny in neighbors:
                        neighbor = self.get_cell_at_location(nx, ny)
                        if neighbor is not None and neighbor.type in ['road', 'v-road', '+-road', 'cornerroad', 't-road', 'endroad' ]: 
                            if nx != x:  
                                horizontal_neighbors += 1
                            if ny != y:  
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
                    elif horizontal_neighbors + vertical_neighbors == 1:
                        cell.set_type('endroad')
                        if self.get_cell_at_location(x, y - self.grid_size) is None:
                            cell.set_rotation(0)
                        elif self.get_cell_at_location(x, y + self.grid_size) is None:
                            cell.set_rotation(180)
                        elif self.get_cell_at_location(x - self.grid_size, y) is None:
                            cell.set_rotation(270)
                        elif self.get_cell_at_location(x + self.grid_size, y) is None:
                            cell.set_rotation(90)
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
        if self.is_building_already_present(x // self.grid_size, y // self.grid_size):
            return None
            
        x = x + 60
        y = y + 60

        road = Road(x, y, self.grid_size)
        road.set_type('road')

        self.play_place_fx()

        self.game_state.placed_objects.append(road)
        for obj in self.game_state.placed_objects:
            print(obj.x, obj.y)
        self.game_state.remove_money(50)
        self.game_state.remove_climate_score(1)
        self.occupied_cells.add((x - 60, y - 60))

        self.connect_nearby_roads(x, y)

        return road
    
    def play_place_fx(self):
        self.placesound.set_volume(0.5)
        self.placesound.play()

        under_construction_image = pygame.image.load('assets/underconstruct.png')
        new_size = (self.window.get_width() // 2, self.window.get_height() // 2)
        under_construction_image = pygame.transform.scale(under_construction_image, new_size)

        screen_center = (self.window.get_width() // 2, self.window.get_height() // 2)
        image_position = (screen_center[0] - under_construction_image.get_width() // 2, 
                        screen_center[1] - under_construction_image.get_height() // 2)

        self.window.blit(under_construction_image, image_position)

        pygame.time.delay(10)
        pygame.display.update()
        
 
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

        self.set_road_image(x, y, 'road.png')

    def set_road_image(self, x, y, image_path):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Road) and obj.x == x and obj.y == y:
                print(f"Setting road image at ({x}, {y}) to {image_path}")
                if image_path == 'v-road.png' or image_path == 'cornerroad.png':
                    new_image = pygame.image.load(image_path)
                else:
                    original_image = pygame.image.load(image_path)
                    new_image = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
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
            placesound = pygame.mixer.Sound('./Sounds/Place.mp3')
            placesound.set_volume(0.5)
            placesound.play()
            self.game_state.remove_money(2000)
            self.game_state.add_climate_score(10)
            self.selected_cell = None
        else:
            print("Not enough money to place an energy building.")
        self.menu_bar_visible = False

    def get_menu_position(self):
        for x in range(32):
            for y in range(17):
                if self.selected_cell[0] == x * self.grid_size and self.selected_cell[1] == y * self.grid_size:
                    if y == 16:  # If the cell is in the bottom row
                        menu_x = self.selected_cell[0] + self.grid_size 
                        menu_y = self.selected_cell[1] - self.grid_size
                    elif x == 0 and y == 16:  # If the cell is in the bottom left corner
                        menu_x = self.selected_cell[0] + self.grid_size 
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    elif x == 31 and y == 0:  # If the cell is in the upper right corner
                        menu_x = self.selected_cell[0] - 160
                        menu_y = self.selected_cell[1] + self.grid_size
                    elif x == 0:  # If the cell is in the leftmost column
                        menu_x = self.selected_cell[0] + self.grid_size
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    elif x == 31:  # If the cell is in the rightmost column
                        menu_x = self.selected_cell[0] - 160
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    else:
                        menu_x = self.selected_cell[0] - 80 + self.grid_size // 2  
                        menu_y = self.selected_cell[1] + self.grid_size
                    return menu_x, menu_y
            
    def draw_building_clicked_menu(self):
        # Load the icons
        upgrade_icon = pygame.image.load('./assets/resources/icons/upgrade.png')
        remove_icon = pygame.image.load('./assets/resources/icons/remove.png')

        # Resize the icons
        icon_width = 30
        icon_height = 30
        upgrade_icon = pygame.transform.scale(upgrade_icon, (icon_width, icon_height))
        remove_icon = pygame.transform.scale(remove_icon, (icon_width, icon_height))

        # if selected cell is on the bottom line, place the menu above the grid cell
        for x in range(32):
            for y in range(17):
                if self.selected_cell[0] == x * self.grid_size and self.selected_cell[1] == y * self.grid_size:
                    if y == 16:  # If the cell is in the bottom row
                        menu_x = self.selected_cell[0] + self.grid_size 
                        menu_y = self.selected_cell[1] - self.grid_size
                    elif x == 0 and y == 16:  # If the cell is in the bottom left corner
                        menu_x = self.selected_cell[0] + self.grid_size 
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    elif x == 31 and y == 0:  # If the cell is in the upper right corner
                        menu_x = self.selected_cell[0] - 160
                        menu_y = self.selected_cell[1] + self.grid_size
                    elif x == 0:  # If the cell is in the leftmost column
                        menu_x = self.selected_cell[0] + self.grid_size
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    elif x == 31:  # If the cell is in the rightmost column
                        menu_x = self.selected_cell[0] - 160
                        menu_y = self.selected_cell[1] - 80 + self.grid_size // 2
                    else:
                        menu_x = self.selected_cell[0] - 80 + self.grid_size // 2  
                        menu_y = self.selected_cell[1] + self.grid_size
                    break
            else:
                continue
            break

        pygame.draw.rect(self.window, (230, 230, 230), (menu_x, menu_y, 160, 50))  

        border_width = 2  
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
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Tree)
        if upgrade_cost is None:
            upgrade_cost = self.get_upgrade_cost(Firestation)

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

        self.draw_effect_range()
        self.draw_house_happiness(menu_x, menu_y)
        
    def draw_house_happiness(self, menu_x, menu_y):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, House) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                if obj.inhab_happiness > 1:
                    happiness_icon = pygame.image.load('./assets/resources/icons/happyhouse.png')
                    happiness_icon = pygame.transform.scale(happiness_icon, (30, 30))
                    self.window.blit(happiness_icon, (menu_x + 65, menu_y - 100))
                elif obj.inhab_happiness <= 1:
                    happiness_icon = pygame.image.load('./assets/resources/icons/sadhouse.png')
                    happiness_icon = pygame.transform.scale(happiness_icon, (30, 30))
                    self.window.blit(happiness_icon, (menu_x + 65, menu_y - 100))

    def draw_effect_range(self):
        for obj in self.game_state.placed_objects:
            if isinstance(obj, Hospital) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                effect_range = obj.effect_range
                pygame.draw.rect(self.window, (180, 255, 180), (obj.x - (effect_range*self.res.GRID_SIZE), obj.y - (effect_range*self.res.GRID_SIZE), self.grid_size + (effect_range*self.res.GRID_SIZE) * 2, self.grid_size + (effect_range*self.res.GRID_SIZE) * 2), 2)
            if isinstance(obj, Factory) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                effect_range = obj.effect_range
                pygame.draw.rect(self.window, (255, 255, 0), (obj.x - (effect_range*self.res.GRID_SIZE), obj.y - (effect_range*self.res.GRID_SIZE), self.grid_size + (effect_range*self.res.GRID_SIZE) * 2, self.grid_size + (effect_range*self.res.GRID_SIZE) * 2), 2)
            if isinstance(obj, Tree) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                effect_range = obj.effect_range
                pygame.draw.rect(self.window, (180, 255, 180), (obj.x - (effect_range*self.res.GRID_SIZE), obj.y - (effect_range*self.res.GRID_SIZE), self.grid_size + (effect_range*self.res.GRID_SIZE) * 2, self.grid_size + (effect_range*self.res.GRID_SIZE) * 2), 2)
            if isinstance(obj, Firestation) and obj.x == self.selected_cell[0] and obj.y == self.selected_cell[1]:
                effect_range = obj.effect_range
                pygame.draw.rect(self.window, (255, 0, 0), (obj.x - (effect_range*self.res.GRID_SIZE), obj.y - (effect_range*self.res.GRID_SIZE), self.grid_size + (effect_range*self.res.GRID_SIZE) * 2, self.grid_size + (effect_range*self.res.GRID_SIZE) * 2), 2)

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


