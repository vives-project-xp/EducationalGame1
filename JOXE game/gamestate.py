class Gamestate:
    def __init__(self):
        self.amountOfCitizens = 0
        self.amountOfHouses = 0
        self.money = 0

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
