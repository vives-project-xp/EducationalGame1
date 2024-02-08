import pygame
from game import Game
from gamestate import Gamestate
import os
import sys

pygame.init()

#WIDTH, HEIGHT = 1920, 1000
WIDTH, HEIGHT = 1420, 800
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)

FPS = 60
GRID_SIZE = 60

def main(window):
    clock = pygame.time.Clock()
    gamestate = Gamestate()
    game = Game(window, WIDTH, HEIGHT, GRID_SIZE, gamestate)
    run = True

    while run:
        clock.tick(FPS)
        game.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game.handle_click(x, y)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(window)