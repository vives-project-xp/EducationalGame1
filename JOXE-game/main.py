import pygame
from game import Game
from gamestate import Gamestate
from tracker import Tracker
# from car import Car
import datetime
import os
import sys
from pygame import mixer

pygame.init()


WIDTH, HEIGHT = 1152, 600


WIDTH, HEIGHT = 1920, 1000
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)


# mixer.init()
# mixer.music.load('Sounds/AmbientLoop1.mp3')
# mixer.music.play(-1)

FPS = 60
GRID_SIZE = WIDTH//32

def main(window):
    clock = pygame.time.Clock()
    gamestate = Gamestate()
    game = Game(window, WIDTH, HEIGHT, GRID_SIZE, gamestate)
    tracker = Tracker(game)

    # car = Car(GRID_SIZE, gamestate.placed_objects)

    run = True
    while run:
        clock.tick(FPS)
        game.draw()
        game.print_game_grid()

        tracker.update()
        average_money_gain, average_ecoscore_change = tracker.get_averages()
        game.draw_averages(average_money_gain, average_ecoscore_change)

        # car.update()

        pygame.display.update()

        elapsed_time = pygame.time.get_ticks() - game.start_time
        game.total_elapsed_time += elapsed_time
        game.start_time = pygame.time.get_ticks()  # Reset the start time

        # If 2 seconds (2,000 milliseconds) have passed
        if game.total_elapsed_time >= 2000:
            game.current_date += datetime.timedelta(days=1)  # Advance the date by one day
            game.total_elapsed_time -= 2000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game.handle_click(x, y)

    pygame.quit()
    sys.exit()

def menu_screen(window):
    background = pygame.image.load('./assets/resources/background/bg2.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    play_button = pygame.image.load('./assets/resources/background/play.png')

    button_width, button_height = play_button.get_rect().size

    button_x = (WIDTH - button_width) / 2
    button_y = (HEIGHT - button_height) / 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    pygame.time.delay(1000)
                    main(window)

        window.blit(background, (0, 0))
        window.blit(play_button, (button_x, button_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu_screen(window)