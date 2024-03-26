import os
from zobjectfiles.road import Road
from zobjectfiles.house import House
from zobjectfiles.energy import Energy
from zobjectfiles.tree import Tree
from zobjectfiles.store import Store
from zobjectfiles.factory import Factory
from zobjectfiles.hospital import Hospital
from resolution import Resolution
import datetime

class Gamestate:
    def __init__(self):
        self.amountOfCitizens = 0
        self.amountOfHouses = 0
        self.money = 1000000
        self.climateScore = 50
        self.placed_objects = []

        self.username = ""
        self.current_date = datetime.datetime(2022, 1, 1)
        self.res = Resolution()
        self.cell_size = self.res.GRID_SIZE
        self.citizen_happiness = 50
        self.game_over = False

    def save_gamestate(self):
        save_folder = "gamesave/"
        filename = f"{save_folder}{self.username.replace('.', '_')}.txt"

        with open(filename, 'w') as file:
            file.write(f"Amount of Citizens: {int(self.amountOfCitizens)}\n")
            file.write(f"Amount of Houses: {int(self.amountOfHouses)}\n")
            file.write(f"Money: {int(self.money)}\n")
            file.write(f"Climate Score: {int(self.climateScore)}\n")
            file.write(f"Current Date: {self.current_date.strftime('%Y-%m-%d')}\n")
            file.write(f"citizen_happiness: {int(self.citizen_happiness)}\n")
            file.write("Placed Objects:\n")
            for obj in self.placed_objects:
                file.write(f"{obj.__class__.__name__}")
                file.write(f"- {obj.level}")
                file.write(f"({obj.x}-{obj.y})")
                if obj.__class__.__name__ == "Road":
                    file.write(f"{obj.type}|{obj.rotation}\n")
                else:
                    file.write("\n")

    def load_gamestate(self):
        save_folder = "gamesave/"
        filename = f"{save_folder}{self.username.replace('.', '_')}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()

            self.amountOfCitizens = int(lines[0].split(": ")[1])
            self.amountOfHouses = int(lines[1].split(": ")[1])
            self.money = int(lines[2].split(": ")[1])
            self.climateScore = float(lines[3].split(": ")[1])
            self.current_date = datetime.datetime.strptime(lines[4].split(": ")[1].strip(), '%Y-%m-%d')
            self.citizen_happiness = int(lines[5].split(": ")[1])

            # Inside the load_gamestate method
            for line in lines[7:]:
                obj_data = line.strip().split('(')
                obj_name, level = obj_data[0].split('-')
                obj_name = obj_name.strip()
                level = int(level.strip())
                coords = obj_data[1].split(')')[0]
                coordinates = coords.split('-')
                if len(coordinates) == 2:
                    x, y = map(int, map(float, map(str.strip, coordinates)))
                else:
                    print(f"Error: Invalid coordinates - {coords}")
                    continue
                x = int(x)
                y = int(y)

                if obj_name == "Road":
                    road_type, rotation = obj_data[1].split(')')[1].split('|')
                    rotation = int(rotation.strip())
                    road_type = road_type.strip()
                    obj = Road(x+10, y+10, self.res.GRID_SIZE, level, rotation)
                    #update image
                    obj.set_type(road_type)
                    obj.update_image()
                    
                elif obj_name == "House":
                    obj = House(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*1000)
                elif obj_name == "Energy":
                    obj = Energy(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*5000)
                elif obj_name == "Tree":
                    obj = Tree(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*1000)
                elif obj_name == "Store":
                    obj = Store(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*3000)
                elif obj_name == "Factory":
                    obj = Factory(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*50000)
                elif obj_name == "Hospital":
                    obj = Hospital(x, y, self.res.GRID_SIZE, level, upgrade_cost= (5**(level-1))*15000)
                else:
                    continue

                self.placed_objects.append(obj)


    def add_object(self, obj):
        self.placed_objects.append(obj)

    def remove_object(self, obj):
        self.placed_objects.remove(obj)

    def add_citizen(self, amount):
        self.amountOfCitizens += amount

    def remove_citizen(self, amount):
        self.amountOfCitizens -= amount

    def add_house(self, amount):
        self.amountOfHouses += amount

    def remove_house(self, amount):
        self.amountOfHouses -= amount

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        self.money -= amount

    def add_climate_score(self, amount):
        if self.climateScore + amount <= 100:
            self.climateScore += amount
        else:
            self.climateScore = 100

    def remove_climate_score(self, amount):
        if self.climateScore - amount >= 0:
            self.climateScore -= amount
        else:
            self.climateScore = 0

    def get_citizen_count(self):
        return self.amountOfCitizens
    
    def update_city_happiness(self, new_happiness):
        self.citizen_happiness = new_happiness
    
    def restart(self):
        self.amountOfCitizens = 0
        self.amountOfHouses = 0
        self.money = 1000
        self.climateScore = 50
        self.placed_objects = []
        self.current_date = datetime.datetime(2022, 1, 1)
        self.citizen_happiness = 50