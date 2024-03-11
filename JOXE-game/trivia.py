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
        close_button_rect = self.show_trivia_popup(self.trivia)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button_rect.collidepoint(pygame.mouse.get_pos()):
                        return

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
        trivia_text = str(trivia)

        # Define popup properties
        popup_width = WIDTH // 3
        popup_height = HEIGHT // 3
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2

        # Create popup (a rectangle with white background and black border)
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.window, (0, 0, 0), popup_rect)  # Black border
        pygame.draw.rect(self.window, (255, 255, 255), popup_rect, 3)  # White background

        # Define close button properties
        close_button_size = 20
        close_button_x = popup_x + popup_width - close_button_size
        close_button_y = popup_y
        close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)

        # Draw close button (a smaller rectangle in the top-right corner of the popup)
        pygame.draw.rect(self.window, (255, 0, 0), close_button_rect)

        # Make the close button image fit well in the close button box 
        close_button_image = pygame.image.load('./assets/resources/icons/close.png')
        close_button_image = pygame.transform.scale(close_button_image, (close_button_size, close_button_size))
        self.window.blit(close_button_image, (close_button_x, close_button_y))
                        
        # Load the image
        mayor_image = pygame.image.load('./assets/resources/characters/Mayor.png')
        mayor_image = pygame.transform.scale(mayor_image, (36 * 5.5, 55 * 5.5))

        # Draw the image onto the popup
        image_x = popup_x + 20  
        image_y = popup_y + 10  
        self.window.blit(mayor_image, (image_x, image_y))
        
        title_font = pygame.font.Font(None, 36)
        title_text = "Did you know?"
        title_rendered = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_rendered.get_rect(center=(popup_x + popup_width // 2, popup_y + 30))
        self.window.blit(title_rendered, title_rect)

        # Render trivia text
        font = pygame.font.Font(None, 26)
        # max width from text should be popup width - 20 (10 padding on each side) and text should be inside the popup, one multiple lines if necessary
        text_surface = pygame.Surface((popup_width - 20, popup_height - 20))
        text_lines = self.wrap_text(trivia_text, text_surface.get_width(), font)
        y_offset = image_y + 120
        for line in text_lines:
            text_rendered = font.render(line, True, (255, 255, 255))
            text_rect = text_rendered.get_rect(topleft=(image_x + mayor_image.get_width() + 10, y_offset))
            self.window.blit(text_rendered, text_rect)
            y_offset += text_rect.height + 5

        # Update the display
        pygame.display.update()

        return close_button_rect

    # Function to wrap text to fit within a specified width
    def wrap_text(self, text, width, font):
        lines = []
        words = text.split()
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_width, _ = font.size(test_line)
            if test_width <= width - (36 * 5.5): # added width of the mayor image
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines