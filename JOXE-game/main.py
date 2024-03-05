import pygame
import random
from game import Game
from gamestate import Gamestate
from tracker import Tracker
from resolution import Resolution
import datetime
import os
import sys
from pygame import mixer
import pygame_menu

pygame.init()
res = Resolution()

WIDTH, HEIGHT = res.width, res.height

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)

FPS = 60


def main(window):
    clock = pygame.time.Clock()
    gamestate = Gamestate()
    game = Game(window, WIDTH, HEIGHT, res.GRID_SIZE, gamestate)
    tracker = Tracker(game)

    run = True
    show_trivia = False
    while run:
        clock.tick(FPS)
        game.draw()
        tracker.update()
        average_money_gain, average_ecoscore_change = tracker.get_averages()
        game.draw_averages(average_money_gain, average_ecoscore_change)
        pygame.display.update()

        elapsed_time = pygame.time.get_ticks() - game.start_time
        game.total_elapsed_time += elapsed_time
        game.start_time = pygame.time.get_ticks()

        if game.total_elapsed_time >= 2000:
            game.current_date += datetime.timedelta(days=1)
            game.total_elapsed_time -= 2000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game.handle_click(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res)

        window.blit(background, (0, 0))
        window.blit(play_button, (button_x, button_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def resolutionWindow(window, main_function, resolution):
    def set_res(resolution_str):
        width, height = map(int, resolution_str.split('x'))
        resolution.set_resolution(width, height)
        window = pygame.display.set_mode((width, height))
        resolutionWindow(window, main_function, resolution)

    def back_to_game():
        main_function(window)

    window_width, window_height = window.get_size()
    menu = pygame_menu.Menu('Resolution', window_width, window_height, theme=pygame_menu.themes.THEME_BLUE)

    for res_option in ['1920x1080', '1920x1000', '1152x600', '800x600', '640x480']:
        menu.add.button(res_option, set_res, res_option)

    menu.add.button('BACK', back_to_game, align=pygame_menu.locals.ALIGN_CENTER)
    
    menu.mainloop(window)


if __name__ == "__main__":
    menu_screen(window)
