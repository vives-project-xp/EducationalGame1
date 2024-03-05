import pygame
from house import House
from road import Road
from resolution import Resolution
import datetime

class Grid:
    def __init__(self, window, grid_size, game_state, font):
        self.window = window
        self.width, self.height = window.get_size()
        self.grid_size = grid_size
        self.game_state = game_state
        self.font = font
        self.start_time = pygame.time.get_ticks()  
        self.total_elapsed_time = 0  
        self.current_date = datetime.datetime(2022, 1, 1) 

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
        self.city_name_logo = pygame.transform.scale(climate_score_logo, (climate_score_logo.get_width() * font_height // climate_score_logo.get_height(), font_height))

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
            # Roads should be displayed one cell above and to the left
            if isinstance(obj, Road):
                self.window.blit(obj.image, (obj.x - self.grid_size, obj.y - self.grid_size))
            else:
                self.window.blit(obj.image, (obj.x, obj.y))

    def draw_game_state(self):
        MARGIN = 50

        # Draw the game state parameters
        citizens_text = self.font.render(f"{self.game_state.amountOfCitizens}", True, (0, 0, 0))
        houses_text = self.font.render(f"{self.game_state.amountOfHouses}", True, (0, 0, 0))
        money_text = self.font.render(f"{self.game_state.money}", True, (0, 0, 0))
        city_name_text = self.font.render(f"{self.game_state.username}", True, (0, 0, 0))

        # Calculate the total width of the text and the margins
        total_width = citizens_text.get_width() + houses_text.get_width() + money_text.get_width() + city_name_text.get_width() + 3 * MARGIN

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
        start_x = 10

        # Calculate resize value for proportional adjustment
        resize_value = self.grid_size / 60

        # Draw the boxes around the logos and the text with proportional adjustment
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 - padding, box_width * resize_value, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 - padding + box_height + MARGIN, box_width * resize_value, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 - padding + 2 * box_height + 2 * MARGIN, box_width * resize_value, box_height + 2 * padding), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (start_x, 10 - padding + 3 * box_height + 3 * MARGIN, box_width * resize_value, box_height + 2 * padding), 2)

        # Draw the logos onto the window with proportional adjustment
        self.window.blit(self.citizens_logo, (start_x + padding, 10))
        self.window.blit(self.houses_logo, (start_x + padding, 10 + box_height + MARGIN))
        self.window.blit(self.money_logo, (start_x + padding, 10 + 2 * box_height + 2 * MARGIN))
        self.window.blit(self.city_name_logo, (start_x + padding, 10 + 3 * box_height + 3 * MARGIN))

        paddY = 40 * resize_value
        # Draw the text onto the window with proportional adjustment
        self.window.blit(citizens_text, (start_x + self.citizens_logo.get_width() + 2 * padding * resize_value, 10))
        self.window.blit(houses_text, (start_x + padding + paddY, 10 + box_height + MARGIN))
        self.window.blit(money_text, (start_x + padding + paddY, 10 + 2 * box_height + 2 * MARGIN))
        self.window.blit(city_name_text, (start_x + padding + paddY, 10 + 3 * box_height + 3 * MARGIN))

        # Calculate the starting x position for the climate bar with proportional adjustment
        climate_bar_start_x = (self.width - (4 * box_width + 3 * MARGIN)) // 2

        # Define a new variable for the y-coordinate adjustment
        adjust_y = 10  # Adjust this value as needed

        # Draw the climate score bar at the top with proportional adjustment
        pygame.draw.rect(self.window, (0, 0, 0), (climate_bar_start_x, adjust_y, 4 * box_width * resize_value + 3 * MARGIN, box_height), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (climate_bar_start_x + padding * resize_value, adjust_y + padding // 2, 4 * box_width * resize_value + 3 * MARGIN - 2 * padding, box_height - padding), 2)

        # Set the color based on the climate score
        if self.game_state.climateScore >= 30:
            score_color = (0, 150, 0)  # Green
        else:
            score_color = (255, 0, 0)  # Red

        # Draw the score bar with the chosen color at the top with proportional adjustment
        pygame.draw.rect(self.window, score_color, (climate_bar_start_x + padding * resize_value, adjust_y + padding // 2, (4 * box_width * resize_value + 3 * MARGIN - 2 * padding) * self.game_state.climateScore // 100, box_height - padding))
        
        # draw date
        self.draw_date()

    def draw_date(self):
        # Draw the current date on the screen
        text = self.font.render(self.current_date.strftime("%d/%m/%Y"), True, (255, 255, 255))
        self.window.blit(text, (self.width / 10 * 9, 0)) 
