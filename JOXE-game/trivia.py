import random
import pygame
import json

# WIDTH, HEIGHT = 1152, 600
WIDTH, HEIGHT = 1920, 1000

# Load trivia from json file
with open('src/trivia.js') as f:
    trivia_list = json.load(f)

# Function to get a random trivia
def get_random_trivia():
    return random.choice(trivia_list)['fact']

# Function to fit text inside popup box
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width, _ = font.size(word + ' ')
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Function to show trivia popup
def show_trivia_popup(window, trivia):
    # Define popup properties
    popup_width = WIDTH // 90
    popup_height = HEIGHT // 90
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    # Create popup (a rectangle with white background)
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(window, (255, 255, 255), popup_rect)

    # Define close button properties
    close_button_size = 20
    close_button_x = popup_x + popup_width - close_button_size
    close_button_y = popup_y
    close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)

    # Draw close button (a smaller rectangle in the top-right corner of the popup)
    pygame.draw.rect(window, (255, 0, 0), close_button_rect)


    # Render trivia text
    font = pygame.font.Font(None, 16)
    lines = wrap_text(trivia, font, popup_width)
    for i, line in enumerate(lines):
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, popup_y + i * font.get_height()))
        window.blit(text, text_rect)

    # Draw text on popup
    window.blit(text, text_rect)

    return close_button_rect