import pygame
import os
import sys
import random
import time

from grid import Grid

pygame.init()
pygame.display.set_caption('JOXE')

programIcon = pygame.image.load('./assets/logo/JOXEC.png') #add the cut out logo
pygame.display.set_icon(programIcon)

WIDTH, HEIGHT = 1920, 1000 # Set the width and height of the window (WIDTH, HEIGHT)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,31) # Set the position of the window (x,y)
window = pygame.display.set_mode((WIDTH, HEIGHT)) # , pygame.RESIZABLE for resizable window (pygame.fullscreen for fullscreen mode)



FPS = 60
GRID_SIZE = 40  # Define the size of the grid cells

def main(window):
    clock = pygame.time.Clock()
    grid = Grid(window, WIDTH, HEIGHT, GRID_SIZE) 
    run = True

    # Load and scale the image outside the main loop
    house_image = pygame.image.load('./assets/resources/house.png')
    house_image = pygame.transform.scale(house_image, (GRID_SIZE, GRID_SIZE))

    # List to store the positions where the image should be drawn
    house_positions = []

    while run:
        clock.tick(FPS)

        window.fill((255, 255, 255))
        grid.draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.VIDEORESIZE:
                # Check if the new size is the same as the screen resolution
                if event.size == (pygame.display.Info().current_w, pygame.display.Info().current_h):
                    # If it is, switch to fullscreen mode
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the left mouse button, 2 is middle, 3 is right.
                    pos = pygame.mouse.get_pos()  # Returns a tuple of (x, y)
                    grid_x = pos[0] // GRID_SIZE  # Calculate the grid cell x
                    grid_y = pos[1] // GRID_SIZE  # Calculate the grid cell y
                    house_positions.append((grid_x * GRID_SIZE, grid_y * GRID_SIZE))  # Store the position
                    print(pos)

        # Draw the image at all stored positions
        for pos in house_positions:
            window.blit(house_image, pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(window)




