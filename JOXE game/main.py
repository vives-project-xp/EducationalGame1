import pygame
import os
import sys
import random
import time

pygame.init()
pygame.display.set_caption('JOXE')

programIcon = pygame.image.load('./assets/house.png')
pygame.display.set_icon(programIcon)

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

def main(window):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        window.fill((255, 255, 255))
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(window)




