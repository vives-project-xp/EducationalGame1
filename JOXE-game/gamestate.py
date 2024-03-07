import os
from road import Road
from house import House
from energy import Energy
from tree import Tree
from store import Store
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

    def save_gamestate(self):
        save_folder = "gamesave/"
        filename = f"{save_folder}{self.username.replace('.', '_')}.txt"

        with open(filename, 'w') as file:
            file.write(f"Amount of Citizens: {self.amountOfCitizens}\n")
            file.write(f"Amount of Houses: {self.amountOfHouses}\n")
            file.write(f"Money: {self.money}\n")
            file.write(f"Climate Score: {self.climateScore}\n")
            file.write(f"Current Date: {self.current_date.strftime('%Y-%m-%d')}\n")
            file.write("Placed Objects:\n")
            for obj in self.placed_objects:
                file.write(f"{obj.__class__.__name__}")
                file.write(f"- {obj.level}")
                file.write(f"({obj.x}-{obj.y})\n")

    def load_gamestate(self):
        save_folder = "gamesave/"
        filename = f"{save_folder}{self.username.replace('.', '_')}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()

            self.amountOfCitizens = int(lines[0].split(": ")[1])
            self.amountOfHouses = int(lines[1].split(": ")[1])
            self.money = int(lines[2].split(": ")[1])
            self.climateScore = int(lines[3].split(": ")[1])
            self.current_date = datetime.datetime.strptime(lines[4].split(": ")[1].strip(), '%Y-%m-%d')

            for line in lines[6:]:
                print(line)
                obj_data = line.strip().split('(')
                obj_name, level = obj_data[0].split('-')
                obj_name = obj_name.strip()
                level = int(level.strip())
                coords = obj_data[1].split(')')[0]
                coordinates = coords.split('-')
                if len(coordinates) == 2:
                    x, y = map(int, map(str.strip, coordinates))
                else:
                    print(f"Error: Invalid coordinates - {coords}")
                    continue
                x = int(x)
                y = int(y)

                if obj_name == "Road":
                    obj = Road(level, x, y)
                elif obj_name == "House":
                    obj = House(level, x, y)
                elif obj_name == "Energy":
                    obj = Energy(level, x, y)
                elif obj_name == "Tree":
                    obj = Tree(level, x, y)
                elif obj_name == "Store":
                    obj = Store(level, x, y)
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
