from resolution import Resolution
import random
import pygame
import json

res = Resolution()

WIDTH, HEIGHT = res.width, res.height

class Trivia:

    def __init__(self, window):
        self.window = window
        self.trivia_list = self.load_trivia()
        self.trivia = self.get_random_trivia(self.trivia_list)

    def show_trivia(self):
        self.trivia = self.get_random_trivia(self.trivia_list)
        self.show_trivia_popup(self.trivia)

    # Load trivia from json file
    def load_trivia(self):
        with open('src/trivia.json') as f:
            trivia_list = json.load(f)
        return trivia_list

    # Function to get a random trivia
    def get_random_trivia(self, trivia_list):
        return random.choice(trivia_list)['fact']

    # Function to show trivia popup
    def show_trivia_popup( self, trivia):
        # Define popup properties
        popup_width = WIDTH // 90
        popup_height = HEIGHT // 90
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2

        # Create popup (a rectangle with white background)
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.window, (255, 255, 255), popup_rect)

        # Define close button properties
        close_button_size = 20
        close_button_x = popup_x + popup_width - close_button_size
        close_button_y = popup_y
        close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)

        # Draw close button (a smaller rectangle in the top-right corner of the popup)
        pygame.draw.rect(self.window, (255, 0, 0), close_button_rect)

        # Load the image
        mayor_image = pygame.image.load('./assets/resources/characters/Mayor.png')
        # Draw the image onto the screen
        image_x = popup_x + 10  
        image_y = popup_y + 10  
        self.window.blit(mayor_image, (image_x, image_y))

        # Render trivia text
        font = pygame.font.Font(None, 16)
        text = font.render(trivia, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, popup_y + popup_height // 2))
        self.window.blit(text, text_rect)

        # Update the display
        pygame.display.update()

        return close_button_rect

