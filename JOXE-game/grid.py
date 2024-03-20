import pygame
from road import Road

class Grid:
    def __init__(self, window, grid_size, game_state, font):
        self.window = window
        self.width, self.height = window.get_size()
        self.grid_size = grid_size
        self.game_state = game_state
        self.font = font
        self.start_time = pygame.time.get_ticks()  
        self.total_elapsed_time = 0  
        self.current_date = self.game_state.current_date
        self.box_height = 0.037 * self.height
        self.box_width = 0.09375 * self.width
        self.pixel_font = "./src/Grand9K Pixel.ttf"

        # Load the logos
        citizens_logo = pygame.image.load('./assets/resources/icons/person.png')
        climate_score_logo = pygame.image.load('./assets/resources/icons/climate.png')
        background_image = pygame.image.load('./assets/resources/background/grass.jpg')
        self.background_image = pygame.transform.scale(background_image, (self.width, self.height))

        # Calculate the new width and height
        new_width = int(self.box_width / 7)

        # Calculate the new width and height for other logos
        original_width, original_height = citizens_logo.get_size()
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)

        # Scale the citizens logo
        self.citizens_logo = pygame.transform.scale(citizens_logo, (new_width, new_height))

        original_width, original_height = climate_score_logo.get_size()
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)

        self.city_name_logo = pygame.transform.scale(climate_score_logo, (new_width, new_height))

    def draw_grid(self):
        self.draw_background()
        self.draw_grid_lines()
        self.draw_game_state()
        self.draw_objects()

    def update_date(self):
        self.current_date = self.game_state.current_date

    def draw_background(self):
        self.window.blit(self.background_image, (0, 0))

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

    def draw_rounded_rect(surface, rect, color, corner_radius):
        """ Draw a rectangle with rounded corners """
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(f"Both width (rect.width) and height (rect.height) must be larger or equal to 2*corner_radius (2*{corner_radius}).")

        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - 1, rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius - 1), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - 1, rect.bottom - corner_radius - 1), corner_radius)

        pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
        pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))

    def draw_game_state(self):
        MARGIN = self.height / 40.2
        padding = self.width / 192
        start_x = 10

        # Change font size based on window
        font_size = int(self.height / 50)
        font = pygame.font.Font(self.pixel_font, font_size)

        # Render the game state parameters
        city_name_text = font.render(f"{self.game_state.username}", True, (255, 255, 255))
        date_text = font.render(f"{self.current_date.strftime('%d/%m/%Y')}", True, (255, 255, 255))
        citizens_text = font.render(f"{self.game_state.amountOfCitizens}", True, (255, 255, 255))
        money_text = font.render(f"{int(self.game_state.money)}", True, (255, 255, 255))
        happiness_text = font.render(f"{int(self.game_state.citizen_happiness)}", True, (255, 255, 255))

        # Load the image
        box_image = pygame.image.load('./assets/resources/icons/box1.png')
        money_box = pygame.image.load('./assets/resources/icons/MoneyBox.png')
        happy_box = pygame.image.load('./assets/resources/icons/Happybox.png')
        angry_box = pygame.image.load('./assets/resources/icons/AngryBox.png')
        nothappy_box = pygame.image.load('./assets/resources/icons/NotHappyBox.png')
        name_box = pygame.image.load('./assets/resources/icons/CityNameBox.png')
        box1_width = int(self.width / 9.8)

        original_width, original_height = box_image.get_size()
        aspect_ratio = original_height / original_width
        new_height = int(self.box_width * aspect_ratio)

        self.box_image = pygame.transform.scale(box_image, (box1_width, new_height))
        self.money_box = pygame.transform.scale(money_box, (box1_width, new_height))
        self.happy_box = pygame.transform.scale(happy_box, (box1_width, new_height))
        self.angry_box = pygame.transform.scale(angry_box, (box1_width, new_height))
        self.nothappy_box = pygame.transform.scale(nothappy_box, (box1_width, new_height))
        self.name_box = pygame.transform.scale(name_box, (box1_width, new_height))

        # Draw the images in place of the boxes
        self.window.blit(self.name_box, (start_x, 15 - padding))
        self.window.blit(self.box_image, (start_x, 15 - padding + self.box_height + MARGIN))
        self.window.blit(self.box_image, (start_x, 15 - padding + 2 * self.box_height + 2 * MARGIN))
        self.window.blit(self.money_box, (start_x, 15 - padding + 3 * self.box_height + 3 * MARGIN))
        if self.game_state.citizen_happiness < 30:
            self.window.blit(self.angry_box, (start_x, 15 - padding + 4 * self.box_height + 4 * MARGIN))
        elif self.game_state.citizen_happiness < 70:
            self.window.blit(self.nothappy_box, (start_x, 15 - padding + 4 * self.box_height + 4 * MARGIN))
        else:
            self.window.blit(self.happy_box, (start_x, 15 - padding + 4 * self.box_height + 4 * MARGIN))

        # # Draw the logos onto the window with proportional adjustment
        self.window.blit(self.city_name_logo, (start_x + (self.width / 192) + 15, 10 + self.box_height + 1.2 * MARGIN + 5))
        self.window.blit(self.citizens_logo, (start_x + (self.width / 192)+ 15, 10 + 2 * self.box_height + 2.2 * MARGIN + 5))

        # Draw the text onto the window with proportional adjustment
        self.window.blit(city_name_text, (3 * start_x + self.box_width // 2 - city_name_text.get_width() // 2, self.box_height - font_size // 2))

        # Center the texts in the middle of the boxes, horizontally and vertically
        self.window.blit(date_text, ( 3 * start_x + self.box_width // 2 - date_text.get_width() // 2, 10 + self.box_height + 2 * MARGIN - font_size // 2))
        self.window.blit(citizens_text, ( 3 * start_x + self.box_width // 2 - citizens_text.get_width() // 2, 10 + 2 * self.box_height + 3 * MARGIN - font_size // 2))
        self.window.blit(money_text, (4 * start_x + self.box_width // 2 - money_text.get_width() // 2, 10 + 3 * self.box_height + 4 * MARGIN - font_size // 2))
        self.window.blit(happiness_text, (3 * start_x + self.box_width // 2 - happiness_text.get_width() // 2, 10 + 4 * self.box_height + 5 * MARGIN - font_size // 2))
        
        # Calculate the starting x position for the climate bar with proportional adjustment
        climate_bar_start_x = (self.width - (4 * self.box_width + 3 * MARGIN)) // 2

        # Define a new variable for the y-coordinate adjustment
        adjust_y = 10  # Adjust this value as needed

        # Draw the climate score bar at the top with proportional adjustment
        pygame.draw.rect(self.window, (0, 0, 0), (climate_bar_start_x, adjust_y, 4 * self.box_width + 3 * MARGIN, self.box_height), 2)
        pygame.draw.rect(self.window, (0, 0, 0), (climate_bar_start_x + padding, adjust_y + padding // 2, 4 * self.box_width + 3 * MARGIN - 2 * padding, self.box_height - padding), 2)

        # Set the color based on the climate score
        if self.game_state.climateScore >= 30:
            score_color = (0, 150, 0)  # Green
        else:
            score_color = (255, 0, 0)  # Red

        # Draw the score bar with the chosen color at the top with proportional adjustment
        pygame.draw.rect(self.window, score_color, (climate_bar_start_x + padding, adjust_y + padding // 2, (4 * self.box_width + 3 * MARGIN - 2 * padding) * self.game_state.climateScore // 100, self.box_height - padding))

        # Add date to gamestate variable
        self.game_state.current_date = self.current_date
