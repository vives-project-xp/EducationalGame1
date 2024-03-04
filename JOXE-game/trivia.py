from resolution import Resolution
import random
import pygame
import json

res = Resolution()

WIDTH, HEIGHT = res.width, res.height

# Load trivia from json file
with open('src/trivia.json') as f:
    trivia_list = json.load(f)

# Function to get a random trivia
def get_random_trivia():
    return random.choice(trivia_list)['fact']

# Function to show trivia popup
def show_trivia_popup(window, trivia):
    # Define popup properties
    popup_width = 400
    popup_height = 200
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    # Create popup (a rectangle with white background)
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(window, (255, 255, 255), popup_rect)

    # Render trivia text
    font = pygame.font.Font(None, 36)
    text = font.render(trivia, True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Draw text on popup
    window.blit(text, text_rect)