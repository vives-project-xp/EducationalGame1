import pygame
from house import House
from road import Road

class Grid:
    def __init__(self, window, width, height, grid_size, game_state, font):
        self.window = window
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.game_state = game_state
        self.font = font

        # Load the logos
        citizens_logo = pygame.image.load('./assets/resources/icons/person.png')
        houses_logo = pygame.image.load('./assets/resources/icons/house.png')
        money_logo = pygame.image.load('./assets/resources/icons/money.png')
        climate_score_logo = pygame.image.load('./assets/resources/icons/climate.png')

        # Calculate the height of the font
        font_height = self.font.get_height()

        # Scale the logos to the height of the font
        self.citizens_logo = pygame.transform.scale(citizens_logo, (citizens_logo.get_width() * font_height // citizens_logo.get_height(), font_height))
        self.houses_logo = pygame.transform.scale(houses_logo, (houses_logo.get_width() * font_height // houses_logo.get_height(), font_height))
        self.money_logo = pygame.transform.scale(money_logo, (money_logo.get_width() * font_height // money_logo.get_height(), font_height))
        self.climate_score_logo = pygame.transform.scale(climate_score_logo, (climate_score_logo.get_width() * font_height // climate_score_logo.get_height(), font_height))

    def draw_grid(self):
        self.draw_background()
        self.draw_grid_lines()
        self.draw_game_state()
        self.draw_objects()

    def draw_background(self):
        background_image = pygame.image.load('./assets/resources/background/grass.jpg')
        background_image = pygame.transform.scale(background_image, (self.width, self.height))
        self.window.blit(background_image, (0, 0))

    def get_all_cells(self):
        return [obj for obj in self.game_state.placed_objects if isinstance(obj, Road)]

    def draw_grid_lines(self):
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.window, (200, 200, 200), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.window, (200, 200, 200), (0, y), (self.width, y))

    def draw_objects(self):
        for obj in self.game_state.placed_objects:
            self.window.blit(obj.image, (obj.x, obj.y))

    def draw_game_state(self):
        MARGIN = 50

        # Draw the game state parameters
        citizens_text = self.font.render(f"{self.game_state.amountOfCitizens}", True, (0, 0, 0))
        houses_text = self.font.render(f"{self.game_state.amountOfHouses}", True, (0, 0, 0))
        money_text = self.font.render(f"{self.game_state.money}", True, (0, 0, 0))
        climateScore_text = self.font.render(f"{self.game_state.climateScore}", True, (0, 0, 0))

        # Calculate the total width of the text and the margins
        total_width = citizens_text.get_width() + houses_text.get_width() + money_text.get_width() + climateScore_text.get_width() + 3 * MARGIN

        # Calculate the starting x position for the text
        start_x = (self.width - total_width) // 2

        # Define the height and padding for the boxes
        box_height = max(self.citizens_logo.get_height(), self.font.get_height())
        padding = 10

        # Calculate the width of the text with 9 numbers
        max_text_width = self.font.size('999999999')[0]

        # Calculate the width of the box
        box_width = self.citizens_logo.get_width() + max_text_width + 2 * padding

        # Calculate the total width of all boxes and margins
        total_width = 4 * box_width + 3 * MARGIN

        # Calculate the starting x position for the boxes
        start_x = (self.width - total_width) // 2

        # Draw the boxes around the logos and the text
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 - padding, box_width, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x + box_width + MARGIN, 10 - padding, box_width, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x + 2 * box_width + 2 * MARGIN, 10 - padding, box_width, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x + 3 * box_width + 3 * MARGIN, 10 - padding, box_width, box_height + 2 * padding), 2)

        # Draw the logos onto the window
        self.window.blit(self.citizens_logo, (start_x + padding, 10))
        self.window.blit(self.houses_logo, (start_x + box_width + MARGIN + padding, 10))
        self.window.blit(self.money_logo, (start_x + 2 * box_width + 2 * MARGIN + padding, 10))
        self.window.blit(self.climate_score_logo, (start_x + 3 * box_width + 3 * MARGIN + padding, 10))

        # Draw the text onto the window
        self.window.blit(citizens_text, (start_x + self.citizens_logo.get_width() + 2 * padding, 10))
        self.window.blit(houses_text, (start_x + box_width + MARGIN + self.houses_logo.get_width() + 2 * padding, 10))
        self.window.blit(money_text, (start_x + 2 * box_width + 2 * MARGIN + self.money_logo.get_width() + 2 * padding, 10))
        self.window.blit(climateScore_text, (start_x + 3 * box_width + 3 * MARGIN + self.climate_score_logo.get_width() + 2 * padding, 10))

        # Draw the climate score bar
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 + box_height + padding, 4 * box_width + 3 * MARGIN, box_height), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x + padding, 10 + box_height + padding + padding // 2, 4 * box_width + 3 * MARGIN - 2 * padding, box_height - padding), 2)

        # Set the color based on the climate score
        if self.game_state.climateScore >= 30:
            score_color = (0, 150, 0)  # Green
        else:
            score_color = (255, 0, 0)  # Red

        # Draw the score bar with the chosen color
        pygame.draw.rect(self.window, score_color, (start_x + padding, 10 + box_height + padding + padding // 2, (4 * box_width + 3 * MARGIN - 2 * padding) * self.game_state.climateScore // 100, box_height - padding))