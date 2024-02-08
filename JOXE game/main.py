import pygame
from game import Game
from gamestate import Gamestate
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1000
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)

FPS = 60
GRID_SIZE = 60 #keep at 60

def main(window):
    clock = pygame.time.Clock()
    gamestate = Gamestate()
    game = Game(window, WIDTH, HEIGHT, GRID_SIZE, gamestate)

    # Track the time when the last money increment occurred
    last_increment_time = pygame.time.get_ticks()

    run = True
    while run:
        clock.tick(FPS)
        game.draw()

        # Check if 10 seconds have passed since the last increment
        current_time = pygame.time.get_ticks()
        if current_time - last_increment_time >= 1000:  # 10000 milliseconds = 10 seconds
            # Calculate the amount of money to add based on the number of citizens
            
            if game.game_state.get_citizen_count() == 0:
                money_to_add = 10
            else:
                money_to_add = game.game_state.get_citizen_count() * 10
            game.game_state.add_money(money_to_add)
            
            last_increment_time = current_time  # Update the last increment time

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game.handle_click(x, y)

    pygame.quit()
    sys.exit()

def menu_screen(window):
    # Load the full-screen image and the play button image
    background = pygame.image.load('./assets/resources/background/bg2.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Resize the background
    play_button = pygame.image.load('./assets/resources/background/play.png')

    # Get the dimensions of the play button
    button_width, button_height = play_button.get_rect().size

    # Calculate the position of the play button
    button_x = (WIDTH - button_width) / 2
    button_y = (HEIGHT - button_height) / 2

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse click is within the bounds of the play button, start the game
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    pygame.time.delay(1000)  # Delay for 1 second
                    main(window)

        # Draw the full-screen image and the play button
        window.blit(background, (0, 0))
        window.blit(play_button, (button_x, button_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu_screen(window)