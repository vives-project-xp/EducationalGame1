import pygame
from object import Object

class Tree(Object):
    def __init__(self, game_state) -> None:
        super().__init__(game_state)
        self.image = pygame.transform.scale(pygame.image.load('./assets/resources/tree/tree.png'), (GRID_SIZE, GRID_SIZE))