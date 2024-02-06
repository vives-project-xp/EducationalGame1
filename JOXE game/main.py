import pygame
import os
import sys
import random
import time

from grid import Grid
from gamestate import Gamestate

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

    #houses
    house_image = pygame.image.load('./assets/resources/houses/house1.png')
    house_image2 = pygame.image.load('./assets/resources/houses/house2.png')
    house_image3 = pygame.image.load('./assets/resources/houses/house3.png')
    house_image4 = pygame.image.load('./assets/resources/houses/house4.png')

    # Load the road image
    road_image = pygame.transform.scale(pygame.image.load('./assets/resources/road/road.png'), (GRID_SIZE, GRID_SIZE))

    house_images = [
    pygame.transform.scale(pygame.image.load('./assets/resources/houses/house1.png'), (GRID_SIZE, GRID_SIZE)),
    pygame.transform.scale(pygame.image.load('./assets/resources/houses/house2.png'), (GRID_SIZE, GRID_SIZE)),
    pygame.transform.scale(pygame.image.load('./assets/resources/houses/house3.png'), (GRID_SIZE, GRID_SIZE)),
    pygame.transform.scale(pygame.image.load('./assets/resources/houses/house4.png'), (GRID_SIZE, GRID_SIZE))
]

    # Load the background image
    background_image = pygame.image.load('./assets/resources/background/grass.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Dictionary to store the positions where the image should be drawn
    house_positions = {}

    # Dictionary to store the positions where the road image should be drawn
    road_positions = {}

    # Create a game state
    game_state = Gamestate()

    # Create a font object
    font = pygame.font.Font(None, 36)

    while run:
        clock.tick(FPS)

        # Draw the background image onto the window
        window.blit(background_image, (0, 0))

        # Draw the grid
        grid.draw_grid()


        #margin for the text
        MARGIN = 250

        # Render the game state parameters
        citizens_text = font.render(f"Citizens: {game_state.amountOfCitizens}", True, (0, 0, 0))
        houses_text = font.render(f"Houses: {game_state.amountOfHouses}", True, (0, 0, 0))
        money_text = font.render(f"Money: {game_state.money}", True, (0, 0, 0))
        climateScore_text = font.render(f"Climate Score: {game_state.climateScore}", True, (0, 0, 0))

        # Calculate the total width of the text and the margins
        total_width = citizens_text.get_width() + houses_text.get_width() + money_text.get_width() + climateScore_text.get_width() + 3 * MARGIN

        # Calculate the starting x position for the text
        start_x = (WIDTH - total_width) // 2


        # Draw the text onto the window
        window.blit(citizens_text, (start_x, 10))
        window.blit(houses_text, (start_x + citizens_text.get_width() + MARGIN, 10))
        window.blit(money_text, (start_x + citizens_text.get_width() + houses_text.get_width() + 2 * MARGIN, 10))
        window.blit(climateScore_text, (start_x + citizens_text.get_width() + houses_text.get_width() + money_text.get_width() + 3 * MARGIN, 10))

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
                house_pos = None
                if event.button == 1:  # 1 is the left mouse button, 2 is middle, 3 is right.
                    pos = pygame.mouse.get_pos()  # Returns a tuple of (x, y)
                    grid_x = pos[0] // GRID_SIZE  # Calculate the grid cell x
                    grid_y = pos[1] // GRID_SIZE  # Calculate the grid cell y
                    house_pos = (grid_x * GRID_SIZE, grid_y * GRID_SIZE)  # Calculate the house position
                elif event.button == 3:  # 3 is the right mouse button
                    pos = pygame.mouse.get_pos()
                    grid_x = pos[0] // GRID_SIZE
                    grid_y = pos[1] // GRID_SIZE
                    road_pos = (grid_x * GRID_SIZE, grid_y * GRID_SIZE)
                    road_positions[road_pos] = road_image


                # Check if there's already a house at this position
                if house_pos not in house_positions:
                    house_positions[house_pos] = house_images[0]  # Store the position and type of the house
                    game_state.add_house(1)  # Increment the number of houses
                    # game_state.add_citizen(5)  # Add 5 citizens for each new house
                    # game_state.remove_money(100)  # Assume each house costs 100 money
                    print(pos)
                else:
                    # If there's already a house, upgrade it to the next level if not already at max level
                    current_house_index = house_images.index(house_positions[house_pos])
                    if current_house_index < len(house_images) - 1:
                        next_house_index = current_house_index + 1
                        house_positions[house_pos] = house_images[next_house_index]

        # Draw the image at all stored positions
        # Draw the image at all stored positions
        for pos, image in house_positions.items():
            if pos is not None:
                window.blit(image, pos)

        for pos, image in road_positions.items():
            if pos is not None:
                window.blit(image, pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(window)




