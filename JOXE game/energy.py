import pygame 
from object import Object

class Energy(Object):
    def __init__(self, game_state) -> None:
        super().__init__(game_state)
        self.image = pygame.transform.scale(pygame.image.load('./assets/resources/buildings/windmills/windmill2.png'), (self.GRID_SIZE, self.GRID_SIZE))
        self.climateScore = 0
        self.expenses = 0