import pygame
from game import Game
from gamestate import Gamestate
from tracker import Tracker
from resolution import Resolution
import datetime
import os
import sys
import pygame_menu

pygame.init()
res = Resolution()

WIDTH, HEIGHT = res.width, res.height

if getattr(sys, 'frozen', False):
    # If it's a bundled application, check if it's bundled with PyInstaller or cx_Freeze
    if hasattr(sys, '_MEIPASS'):
        # Bundled with PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Bundled with cx_Freeze
        base_dir = os.path.dirname(sys.executable)
else:
    # Not a bundled application, so use the script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path
icon_path = os.path.join(base_dir, 'assets', 'logo', 'JOXEC.png')

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 31)
window = pygame.display.set_mode((WIDTH, HEIGHT))
programIcon = pygame.image.load(icon_path)
pygame.display.set_icon(programIcon)

# # Soundtrack
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm_menu(window, main, gamestate)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if gamestate.game_over:
                    if game.width // 2 - 100 <= x <= game.width // 2 + 100 and game.height // 2 + 200 <= y <= game.height // 2 + 250:
                        game.game_state.restart()
                        game.game_over_timer_start = None
                        game.grid.update_date()
                else:
                    game.handle_click(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res, gamestate)

        if gamestate.game_over:
            game.draw_game_over()
        else:
            clock.tick(FPS)
            game.draw()
            tracker.update()
            average_money_gain, average_ecoscore_change = tracker.get_averages() 
            game.draw_averages(average_money_gain, average_ecoscore_change)
            elapsed_time = pygame.time.get_ticks() - game.grid.start_time
            game.grid.total_elapsed_time += elapsed_time
            game.grid.start_time = pygame.time.get_ticks()

            if game.grid.total_elapsed_time >= 2000:
                game.grid.current_date += datetime.timedelta(days=1)
                game.grid.total_elapsed_time -= 2000

        pygame.display.update()

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
            print("Please enter a cityname!")
            menu.add.label('Please enter a cityname.', font_name='./src/Grand9K Pixel.ttf')
            menu.draw(window)
            pygame.display.update()

    window_width, window_height = window.get_size()
    
    # Create a custom theme
    blackTheme = pygame_menu.themes.Theme(
        widget_font='./src/Grand9K Pixel.ttf',
        background_color=(0, 0, 0),  # Black
        widget_font_color=(255, 255, 255),  # White
        widget_font_size=32,
        widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
            arrow_right_margin=5
        ),
        selection_color=(255, 255, 255)  # White
    )

    menu = pygame_menu.Menu('', window_width, window_height, theme=blackTheme)

    menu.add.label('Welcome to JOXE!', font_name='./src/Grand9K Pixel.ttf', font_size=80)
    menu.add.vertical_margin(80) 
    menu.add.label('Please enter a city name:', font_name='./src/Grand9K Pixel.ttf')
    
    username_input = menu.add.text_input('', default='', maxchar=10, font_name='./src/Grand9K Pixel.ttf', width=200)
    menu.add.vertical_margin(10) 
    menu.add.button('Play', lambda: start_game(username_input.get_value()), font_name='./src/Grand9K Pixel.ttf')
    menu.add.vertical_margin(10) 
    menu.add.button('Quit', pygame_menu.events.EXIT, font_name='./src/Grand9K Pixel.ttf')

    menu.mainloop(window)

def menu_screen(window):
    background = pygame.image.load('./assets/resources/background/bg2.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    play_button = pygame.image.load('./assets/resources/background/play.png')
    pixel_font_path = "./src/Grand9K Pixel.ttf"
    pixel_font = pygame.font.Font(pixel_font_path, 70)

    button_width, button_height = play_button.get_rect().size

    button_x = (WIDTH - button_width) / 2
    button_y = (HEIGHT - button_height) / 2

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_hover:
                    loading_text = pixel_font.render("Loading...", True, (255, 255, 255))
                    window.blit(loading_text, (WIDTH - loading_text.get_width() - 10 , HEIGHT - loading_text.get_height() - 10 ))
                    pygame.display.flip()

                    pygame.time.delay(1000)
                    login_screen(window) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resolutionWindow(window, main, res)

        window.blit(background, (0, 0))
        window.blit(play_button, (button_x, button_y - 10 if button_hover else button_y))

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
    blackTheme = pygame_menu.themes.Theme(
        widget_font='./src/Grand9K Pixel.ttf',
        background_color=(0, 0, 0),  # Black
        widget_font_color=(255, 255, 255),  # White
        widget_font_size=32,
        widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
            arrow_right_margin=5
        ),
        selection_color=(255, 255, 255)  # White
    )

    menu = pygame_menu.Menu('', window_width, window_height, theme=blackTheme)

    menu.add.label('Resolution', font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 15)
    menu.add.vertical_margin(window_height // 20)
    for res_option in ['1920x1080', '1920x1000', '1152x600', '800x416', '640x333']:
        menu.add.button(res_option, set_res, res_option, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 22)

    menu.add.button('Save', save_gamestate, align=pygame_menu.locals.ALIGN_CENTER, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 25)
    menu.add.button('BACK', back_to_game, align=pygame_menu.locals.ALIGN_CENTER, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 25)

    menu.mainloop(window)

# Confirm menu that appears when pressing close button
def confirm_menu(window, main_function, gamestate):
    window_width, window_height = window.get_size()
    blackTheme = pygame_menu.themes.Theme(
        widget_font='./src/Grand9K Pixel.ttf',
        background_color=(0, 0, 0), 
        widget_font_color=(255, 255, 255), 
        widget_font_size= window_height // 20,
        widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
            arrow_right_margin=5
        ),
        selection_color=(255, 255, 255)  # White
    )

    menu = pygame_menu.Menu('', window_width, window_height, theme=blackTheme)

    menu.add.label("We 're sad to see you go :(", font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 15)
    menu.add.vertical_margin(window_height // 20)
    menu.add.label('Do you want to save the game?', font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 20)
    menu.add.vertical_margin(window_height // 20)

    def save_gamestate():
        gamestate.save_gamestate()
        pygame.quit()
        sys.exit()

    menu.add.button('Yes, save', save_gamestate, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 20)

    def go_back():
        main_function(window, gamestate)
    
    menu.add.vertical_margin(window_height // 30)
    menu.add.button('No, continue game', go_back, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 20)
    menu.add.vertical_margin(window_height // 30)
    menu.add.button('No, quit without saving', pygame_menu.events.EXIT, font_name='./src/Grand9K Pixel.ttf', font_size= window_height // 20)

    menu.mainloop(window)
                
if __name__ == "__main__":
    menu_screen(window)