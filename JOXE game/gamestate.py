class Gamestate:
    def __init__(self):
        self.amountOfCitizens = 0
        self.amountOfHouses = 0
        self.money = 30000
        self.climateScore = 92
        self.placed_objects = []

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
        if self.climateScore < 100:
            self.climateScore += amount
        elif self.climateScore + amount > 100:
            self.climateScore = 100

    def remove_climate_score(self, amount):
        if self.climateScore > 0:
            self.climateScore -= amount
        elif self.climateScore - amount < 0:
            self.climateScore = 0
