import pygame
from house import House
from tree import Tree
from energy import Energy
from store import Store
from park import Park
from factory import Factory

class Tracker:
    def __init__(self, game, game_state):
        self.game = game
        self.game_state = game_state
        self.money_multiplier = max(self.game_state.citizen_happiness / 50,0.5)
        self.ecoscore_multiplier = max(self.game_state.citizen_happiness / 50,0.5)
        self.last_update_times = {
            'money': pygame.time.get_ticks(),
            'ecoscore_deduction': pygame.time.get_ticks(),
            'windmill_ecoscore': pygame.time.get_ticks(),
            'windmill_cost': pygame.time.get_ticks(),
            'tree_ecoscore': pygame.time.get_ticks(),
            'store_cost': pygame.time.get_ticks(),
            'store_ecoscore': pygame.time.get_ticks(),
            'factory_cost': pygame.time.get_ticks(),
            'factory_ecoscore': pygame.time.get_ticks(),
            'park_ecoscore': pygame.time.get_ticks(),
            'park_cost': pygame.time.get_ticks(),
        }
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
        self.update_store_cost(current_time)
        self.update_store_ecoscore(current_time)
        self.auto_deduct_ecoscore(current_time)
        self.update_factory_cost(current_time)
        self.update_factory_ecoscore(current_time)
        self.update_park_cost(current_time)
        self.update_park_ecoscore(current_time)

    def auto_deduct_ecoscore(self, current_time):
        if current_time - self.last_update_times['ecoscore_deduction'] >= 2000:
            print(self.ecoscore_multiplier)
            auto_deduct_eco = 0.01 / self.ecoscore_multiplier
            print(auto_deduct_eco)
            self.game.game_state.remove_climate_score(auto_deduct_eco)
            self.total_ecoscore_change -= auto_deduct_eco

    def update_money(self, current_time):
        if current_time - self.last_update_times['money'] >= 1000:
            money_to_add = max(10, self.game.game_state.get_citizen_count() * 10)
            money_to_add *= self.money_multiplier
            self.game.game_state.add_money(money_to_add)
            self.total_money_gain += money_to_add
            self.last_update_times['money'] = current_time

    def update_ecoscore_deduction(self, current_time):
        if current_time - self.last_update_times['ecoscore_deduction'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, House) and obj.level in range(1, 4):
                    climate_score_deduction = 1 / self.ecoscore_multiplier
                    self.game.game_state.remove_climate_score(climate_score_deduction)
                    self.total_ecoscore_change -= climate_score_deduction
            self.last_update_times['ecoscore_deduction'] = current_time

    def update_windmill_ecoscore(self, current_time):
        if current_time - self.last_update_times['windmill_ecoscore'] >= 300000:  # 5 minutes = 300000 milliseconds
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Energy):
                    climate_score_deduction = 3 * self.ecoscore_multiplier
                    self.game.game_state.add_climate_score(climate_score_deduction)
                    self.total_ecoscore_change += climate_score_deduction
                    self.update_windmill_cost(current_time)
                    self.game_state.add_citizen_happiness(1)
            self.last_update_times['windmill_ecoscore'] = current_time

    def update_windmill_cost(self, current_time):
        if (current_time - self.last_update_times['windmill_cost'] >= 60000):  # 1 minute = 60000 milliseconds
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Energy):
                    cost = 300 / self.money_multiplier
                    self.game.game_state.remove_money(cost)
                    self.total_money_gain -= cost
            self.last_update_times['windmill_cost'] = current_time

    def update_tree_ecoscore(self, current_time):
        if current_time - self.last_update_times['tree_ecoscore'] >= 600000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Tree):
                    climate_score_deduction = 1 * self.ecoscore_multiplier
                    self.game.game_state.add_climate_score(climate_score_deduction)
                    self.total_ecoscore_change += climate_score_deduction
                    self.game_state.add_citizen_happiness(1)
            self.last_update_times['tree_ecoscore'] = current_time

    def update_store_cost(self, current_time):
        if current_time - self.last_update_times['store_cost'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Store):
                    cost = 100 * self.money_multiplier
                    self.game.game_state.add_money(cost)
                    self.total_money_gain += cost
            self.last_update_times['store_cost'] = current_time

    def update_store_ecoscore(self, current_time):
        if current_time - self.last_update_times['store_ecoscore'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Store):
                    climate_score_deduction = 5 / self.ecoscore_multiplier
                    self.game.game_state.remove_climate_score(climate_score_deduction)
                    self.total_ecoscore_change -= climate_score_deduction
                    self.game_state.add_citizen_happiness(1)
            self.last_update_times['store_ecoscore'] = current_time

    def update_factory_cost(self, current_time):
        if current_time - self.last_update_times['factory_cost'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Factory):
                    cost = 500 * self.money_multiplier
                    self.game.game_state.add_money(cost)
                    self.total_money_gain += cost
            self.last_update_times['factory_cost'] = current_time

    def update_factory_ecoscore(self, current_time):
        if current_time - self.last_update_times['factory_ecoscore'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Factory):
                    climate_score_deduction = 10 / self.ecoscore_multiplier
                    self.game.game_state.remove_climate_score(climate_score_deduction)
                    self.total_ecoscore_change -= climate_score_deduction
                    self.game_state.remove_citizen_happiness(3)
            self.last_update_times['factory_ecoscore'] = current_time

    def update_park_cost(self, current_time):
        if current_time - self.last_update_times['park_cost'] >= 60000:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Park):
                    cost = 500 / self.money_multiplier
                    self.game.game_state.remove_money(cost)
                    self.total_money_gain -= cost
            self.last_update_times['park_cost'] = current_time

    def update_park_ecoscore(self, current_time):
        if current_time - self.last_update_times['park_ecoscore'] >= 600:
            for obj in self.game.game_state.placed_objects:
                if isinstance(obj, Park):
                    climate_score_deduction = 0.1 * self.ecoscore_multiplier
                    self.game.game_state.add_climate_score(climate_score_deduction * obj.level)
                    self.total_ecoscore_change += (climate_score_deduction * obj.level)
                    self.game_state.add_citizen_happiness(0.01)
            self.last_update_times['park_ecoscore'] = current_time

    def get_averages(self):
        elapsed_minutes = (pygame.time.get_ticks() - self.start_time) / 60000
        average_money_gain = self.total_money_gain / elapsed_minutes
        average_ecoscore_change = self.total_ecoscore_change / elapsed_minutes
        return average_money_gain, average_ecoscore_change
