import os

class Gamestate:
    def __init__(self):
        self.amountOfCitizens = 0
        self.amountOfHouses = 0
        self.money = 1000000
        self.climateScore = 50
        self.placed_objects = []
        self.username = ""

    def save_gamestate(self):
        save_folder = "gamesave/"
        filename = f"{save_folder}{self.username.replace('.', '_')}.txt"

        with open(filename, 'w') as file:
            file.write(f"Amount of Citizens: {self.amountOfCitizens}\n")
            file.write(f"Amount of Houses: {self.amountOfHouses}\n")
            file.write(f"Money: {self.money}\n")
            file.write(f"Climate Score: {self.climateScore}\n")
            file.write("Placed Objects:\n")
            for obj in self.placed_objects:
                file.write(f"- {obj}\n")

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
