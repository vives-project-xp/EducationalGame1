import pygame
from house import House
from tree import Tree
from energy import Energy

class Tracker:
    def __init__(self, game):
        self.game = game
        self.last_increment_time = pygame.time.get_ticks()
        self.last_ecoscore_deduction_time = pygame.time.get_ticks()
        self.last_windmill_ecoscore_time = pygame.time.get_ticks()
        self.last_tree_ecoscore_time = pygame.time.get_ticks()
        self.last_windmill_cost_time = pygame.time.get_ticks()
        self.total_money_gain = 0
        self.total_ecoscore_change = 0
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        self.update_money(current_time)
        self.update_ecoscore_deduction(current_time)
        self.update_windmill_ecoscore(current_time)
        self.update_windmill_cost(current_time)  
        self.update_tree_ecoscore(current_time)

    def update_money(self, current_time):
        if current_time - self.last_increment_time >= 1000:
            money_to_add = max(10, self.game.game_state.get_citizen_count() * 10)
            self.game.game_state.add_money(money_to_add)
            self.total_money_gain += money_to_add
            self.last_increment_time = current_time

    def update_ecoscore_deduction(self, current_time):
        if current_time - self.last_ecoscore_deduction_time >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, House) and obj.level in range(1, 4):
                    self.game.game_state.remove_climate_score(1)
                    self.total_ecoscore_change -= 1
            self.last_ecoscore_deduction_time = current_time

    def update_windmill_ecoscore(self, current_time):
        if current_time - self.last_windmill_ecoscore_time >= 300000:  # 5 minutes = 300000 milliseconds
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Energy):
                    self.game.game_state.add_climate_score(3)
                    self.total_ecoscore_change += 3
                    self.update_windmill_cost(current_time)
            self.last_windmill_ecoscore_time = current_time

    def update_windmill_cost(self, current_time):
        if (current_time - self.last_windmill_cost_time >= 60000):  # 1 minute = 60000 milliseconds
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Energy):
                    self.game.game_state.remove_money(300)
                    self.total_money_gain -= 300
            self.last_windmill_cost_time = current_time

    def update_tree_ecoscore(self, current_time):
        if current_time - self.last_tree_ecoscore_time >= 600000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Tree):
                    self.game.game_state.add_climate_score(1)
                    self.total_ecoscore_change += 1
            self.last_tree_ecoscore_time = current_time

    def get_averages(self):
        elapsed_minutes = (pygame.time.get_ticks() - self.start_time) / 60000
        average_money_gain = self.total_money_gain / elapsed_minutes
        average_ecoscore_change = self.total_ecoscore_change / elapsed_minutes
        return average_money_gain, average_ecoscore_change