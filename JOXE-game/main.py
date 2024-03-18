import pygame
from game import Game
from gamestate import Gamestate
from tracker import Tracker
from resolution import Resolution
from ownUIelements import Slider
import datetime
import os
import sys
import pygame_menu

pygame.init()
res = Resolution()

WIDTH, HEIGHT = res.width, res.height

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load('./assets/logo/JOXEC.png')
pygame.display.set_icon(programIcon)


# pygame.mixer.init()
# sound = pygame.mixer.Sound('./Sounds/AmbientLoop1.mp3')
# sound.set_volume(0.5)
# sound.play()

FPS = 60

def main(window, gamestate):
    clock = pygame.time.Clock()
    game = Game(window, res.GRID_SIZE, gamestate)
    tracker = Tracker(game, gamestate)

    run = True
    while run:
        clock.tick(FPS)
        game.draw()
        tracker.update()
        average_money_gain, average_ecoscore_change = tracker.get_averages()
        game.draw_averages(average_money_gain, average_ecoscore_change)
        pygame.display.update()

        elapsed_time = pygame.time.get_ticks() - game.grid.start_time
        game.grid.total_elapsed_time += elapsed_time
        game.grid.start_time = pygame.time.get_ticks()

        if game.grid.total_elapsed_time >= 2000:
            game.grid.current_date += datetime.timedelta(days=1)
            game.grid.total_elapsed_time -= 2000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game.handle_click(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res, gamestate)

    pygame.quit()
    sys.exit()

def login_screen(window):
    def start_game(username):
        if username:
            gamestate = Gamestate()
            gamestate.username = username
            gamestate.load_gamestate() 
            print(f"Starting game for user {username}")
            main(window, gamestate)
        else:
            print("Please enter a username.")

    window_width, window_height = window.get_size()
    menu = pygame_menu.Menu('Login', window_width, window_height, theme=pygame_menu.themes.THEME_BLUE)

    menu.add.label('City name:')
    
    username_input = menu.add.text_input('', default='..........', maxchar=10)
    
    menu.add.button('Play', lambda: start_game(username_input.get_value()))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(window)


def menu_screen(window):
    background = pygame.image.load('./assets/resources/background/bg2.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    play_button = pygame.image.load('./assets/resources/background/play.png')

    button_width, button_height = play_button.get_rect().size

    btn_x = (WIDTH - button_width) / 2
    btn_y = (HEIGHT - button_height) / 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if btn_x <= mouse_x <= btn_x + button_width and btn_y <= mouse_y <= btn_y + button_height:
                    pygame.time.delay(1000)
                    login_screen(window) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res)

        window.blit(background, (0, 0))
        window.blit(play_button, (btn_x, btn_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def resolutionWindow(window, main_function, resolution, gamestate):
    def set_res(resolution_str):
        width, height = map(int, resolution_str.split('x'))
        resolution.set_resolution(width, height)
        window = pygame.display.set_mode((width, height))
        resolutionWindow(window, main, resolution, gamestate)

    def back_to_game():
        main_function(window, gamestate)    

    def save_gamestate():
        gamestate.save_gamestate()
        back_to_game()

    window_width, window_height = window.get_size()
    menu = pygame_menu.Menu('Resolution', window_width, window_height, theme=pygame_menu.themes.THEME_BLUE)

    for res_option in ['1920x1080', '1920x1000', '1152x600', '800x416', '640x333']:
        menu.add.button(res_option, set_res, res_option)

    menu.add.button('Save', save_gamestate, align=pygame_menu.locals.ALIGN_CENTER)  
    menu.add.button('BACK', back_to_game, align=pygame_menu.locals.ALIGN_CENTER)

    # slider = Slider(100, 100, 200, 0, 1)

    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         slider.handle_event(event)

    #     window.fill((0, 0, 0))
    #     slider.draw(window)
    #     pygame.display.flip()

    menu.mainloop(window)

if __name__ == "__main__":
    menu_screen(window)
