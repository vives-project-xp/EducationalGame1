import pygame
import os
import sys
import random
import time

from grid import Grid

pygame.init()
pygame.display.set_caption('JOXE')

programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
GRID_SIZE = 40  # Define the size of the grid cells

def main(window):
    clock = pygame.time.Clock()
    grid = Grid(window, WIDTH, HEIGHT, GRID_SIZE) 
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the left mouse button, 2 is middle, 3 is right.
                    pos = pygame.mouse.get_pos()  # Returns a tuple of (x, y)
                    print(pos)

        window.fill((255, 255, 255))
        grid.draw_grid() 
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(window)




