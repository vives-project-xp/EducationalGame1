from resolution import Resolution
import random
import pygame
import json

res = Resolution()

WIDTH, HEIGHT = res.width, res.height

class Trivia:

    def __init__(self, window, game_state):
        self.window = window
        self.width, self.height = window.get_size()
        self.trivia_list = self.load_trivia()
        self.trivia = self.get_random_trivia(self.trivia_list)
        self.game_state = game_state
        self.pixel_font = "./src/Grand9K Pixel.ttf"

    def show_trivia(self):
        self.trivia = self.get_random_trivia(self.trivia_list)
        close_button_rect, answer_buttons = self.show_trivia_popup(self.trivia)
        correct_answer_index = self.trivia['answers'].index(self.trivia['correct'])
        answer_selected = False
        selected_answer_index = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if close button is pressed or the user clicks outside the popup, close the popup
                    if close_button_rect.collidepoint(pygame.mouse.get_pos()): 
                        return
                    # if an answer button is clicked, check if it's the correct answer
                    for i, answer_button in enumerate(answer_buttons):
                        if answer_button.collidepoint(pygame.mouse.get_pos()):
                            selected_answer_index = i
                            answer_selected = True
                            if selected_answer_index == correct_answer_index:
                                self.game_state.add_money(100000)
                                print("True")
                            else:
                                print("False")
                            break

            # Draw a white border around the answer button that the mouse is hovering on
            mouse_pos = pygame.mouse.get_pos()
            for i, answer_button in enumerate(answer_buttons):
                if answer_selected:
                    if i == correct_answer_index:
                        pygame.draw.rect(self.window, (0, 255, 0), answer_button, 1)  # Green border for correct answer
                    if i == selected_answer_index and i != correct_answer_index:
                        pygame.draw.rect(self.window, (255, 0, 0), answer_button, 1)  # Red border for incorrect answer
                else:
                    if answer_button.collidepoint(mouse_pos):
                        pygame.draw.rect(self.window, (255, 255, 255), answer_button, 1)
                    else:
                        pygame.draw.rect(self.window, (0, 0, 0), answer_button, 1)

            pygame.display.update()      

    # Load trivia from json file
    def load_trivia(self):
        with open('src/trivia1.json', 'r', encoding='utf-8') as f:
            trivia_list = json.load(f)
        return trivia_list

    # Function to get a random trivia
    def get_random_trivia(self, trivia_list):
        return random.choice(trivia_list)

    # Function to show trivia popup
    def show_trivia_popup( self, trivia):

        # Define popup properties
        popup_width = self.width // 1.5
        popup_height = self.height // 1.5
        popup_x = (self.width - popup_width) // 2
        popup_y = (self.height - popup_height) // 2

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
        image_width = int(popup_width // 5)
        image_height = int(image_width * (55 / 36))

        # If the calculated height is greater than the desired maximum height
        if image_height > popup_height // 3:
            image_height = int(popup_height // 3)
            image_width = int(image_height * (36 / 55)) 

        mayor_image = pygame.transform.scale(mayor_image, (image_width, image_height))

        # Draw the image onto the popup
        image_x = popup_x + 20  
        image_y = popup_y + 10  
        self.window.blit(mayor_image, (image_x, image_y))
        
        title_font = pygame.font.Font(self.pixel_font, self.width // 30)
        title_text = "Do you know?"
        title_rendered = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_rendered.get_rect(center=(popup_x + popup_width // 2, popup_y + 30))
        self.window.blit(title_rendered, title_rect)

        # Render trivia question 
        question_font = pygame.font.Font(None, self.width // 50)
        question_text = trivia['question']
        wrapped_question_text = self.wrap_text(question_text, popup_width - image_width - 40, question_font) 
        question_y = image_y + 120
        for line in wrapped_question_text:
            question_rendered = question_font.render(line, True, (255, 255, 255))
            question_rect = question_rendered.get_rect(topleft=(image_x + mayor_image.get_width() + 10, question_y))
            self.window.blit(question_rendered, question_rect)
            question_y += question_font.get_height()  

        # Render answer options as buttons
        answer_font = pygame.font.Font(None, self.width // 60)
        answer_buttons = []
        answer_y = question_rect.bottom + 20
        for i, answer in enumerate(trivia['answers']):
            answer_text = answer
            wrapped_answer_text = self.wrap_text(answer_text, popup_width - image_width - 40, answer_font) 
            answer_start_y = answer_y 
            max_width = 0
            for line in wrapped_answer_text:
                answer_rendered = answer_font.render(line, True, (255, 255, 255))
                answer_rect = answer_rendered.get_rect(topleft=(image_x + mayor_image.get_width() + 10, answer_y))
                self.window.blit(answer_rendered, answer_rect)
                answer_y += answer_font.get_height()  
                if answer_rect.width > max_width: 
                    max_width = answer_rect.width 
            # Create a rectangle that encompasses all the lines of the answer
            answer_button = pygame.Rect(answer_rect.left, answer_start_y, max_width, answer_y - answer_start_y)
            answer_buttons.append(answer_button)
            answer_y += 30  # Add some space between answers

        # Update the display
        pygame.display.update()

        return close_button_rect, answer_buttons

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
    