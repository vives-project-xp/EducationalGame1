import pygame
import sys

class Player():
    def __init__(self, name):
        self.name = name
        self.population = 0
        self.pollution = 0

    def add_population(self, amount):
        self.population += amount

    def remove_population(self, amount):
        if self.population - amount >= 0:
            self.population -= amount
        else:
            self.population = 0

    def add_pollution(self, amount):
        self.pollution += amount

    def remove_pollution(self, amount):
        if self.pollution - amount >= 0:
            self.pollution -= amount
        else:
            self.pollution = 0

def draw_player_info(screen, player, x, y, width):
    font = pygame.font.Font(None, 36)
    name_text = font.render(f"{player.name}", 1, (10, 10, 10))
    population_text = font.render(f"{player.population}", 1, (10, 10, 10))
    pollution_text = font.render(f"{player.pollution}", 1, (10, 10, 10))

    name_text_rect = name_text.get_rect(center=(x + width / 2, y + 5))  
    population_text_rect = population_text.get_rect(center=(x + width / 2, y + 40 + 5)) 
    pollution_text_rect = pollution_text.get_rect(center=(x + width / 2, y + 80 + 5))  

    screen.blit(name_text, name_text_rect)
    screen.blit(population_text, population_text_rect)
    screen.blit(pollution_text, pollution_text_rect)

    # Draw "+" and "-" buttons for population
    draw_button(screen, "-", x + width / 2 - 50, y + 40, 20, 20, (255, 0, 0))
    draw_button(screen, "+", x + width / 2 + 50, y + 40, 20, 20, (0, 255, 0))

    # Draw "+" and "-" buttons for pollution
    draw_button(screen, "-", x + width / 2 - 50, y + 80, 20, 20, (255, 0, 0))
    draw_button(screen, "+", x + width / 2 + 50, y + 80, 20, 20, (0, 255, 0))

def draw_total_population_and_pollution(screen, players, x, y, max_bar_value=40):
    total_population = sum(player.population for player in players)
    total_pollution = sum(player.pollution for player in players)

    # Define the dimensions of the bar
    bar_width = 200
    bar_height = 20

    # Calculate the length of the population and pollution bars
    population_bar_length = min((total_population / max_bar_value) * bar_width, bar_width)
    pollution_bar_length = min((total_pollution / max_bar_value) * bar_width, bar_width)

    # Draw the background of the bars
    pygame.draw.rect(screen, (255, 255, 255), (x - bar_width / 2, y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (x - bar_width / 2, y + 40, bar_width, bar_height))

    # Draw the population and pollution bars
    pygame.draw.rect(screen, (0, 255, 0), (x - bar_width / 2, y, population_bar_length, bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (x - bar_width / 2, y + 40, pollution_bar_length, bar_height))

    # Draw a border around the bars
    border_color = (0, 0, 0)  # Black color
    border_thickness = 2  # You can change this to whatever you like
    pygame.draw.rect(screen, border_color, (x - bar_width / 2, y, bar_width, bar_height), border_thickness)
    pygame.draw.rect(screen, border_color, (x - bar_width / 2, y + 40, bar_width, bar_height), border_thickness)

    # Create font object
    font = pygame.font.Font(None, 24)  # Change the number for different font sizes

    # Create text surfaces for total population and pollution
    population_text = font.render(str(total_population), True, (0, 0, 0))
    pollution_text = font.render(str(total_pollution), True, (0, 0, 0))

    # Get rectangles for positioning text
    population_text_rect = population_text.get_rect(center=(x, y + bar_height / 2))
    pollution_text_rect = pollution_text.get_rect(center=(x, y + 40 + bar_height / 2))

    # Blit the text onto the screen
    screen.blit(population_text, population_text_rect)
    screen.blit(pollution_text, pollution_text_rect)
    
def handle_player_info_button(event, player, x, y, width):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if click is within "-" button for population
        if x + width / 2 - 50 <= event.pos[0] <= x + width / 2 - 30 and y + 40 <= event.pos[1] <= y + 60:
            player.remove_population(1)
            print(f"Decreased {player.name}'s population to {player.population}")
        # Check if click is within "+" button for population
        elif x + width / 2 + 50 <= event.pos[0] <= x + width / 2 + 70 and y + 40 <= event.pos[1] <= y + 60:
            player.add_population(1)
            print(f"Increased {player.name}'s population to {player.population}")
        # Check if click is within "-" button for pollution
        elif x + width / 2 - 50 <= event.pos[0] <= x + width / 2 - 30 and y + 80 <= event.pos[1] <= y + 100:
            player.remove_pollution(1)
            print(f"Decreased {player.name}'s pollution to {player.pollution}")
        # Check if click is within "+" button for pollution
        elif x + width / 2 + 50 <= event.pos[0] <= x + width / 2 + 70 and y + 80 <= event.pos[1] <= y + 100:
            player.add_pollution(1)
            print(f"Increased {player.name}'s pollution to {player.pollution}")

def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text, text_rect)

def handle_next_round_button(event, x, y, width, height):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if x <= event.pos[0] <= x + width and y <= event.pos[1] <= y + height:
            print("Next round button clicked")
            return True
    return False

def draw_player_count(screen, player_count, x, y):
    font = pygame.font.Font(None, 80)
    text = font.render(f"{player_count}", 1, (10, 10, 10))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect) 

def handle_events(players):
    start_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_width, button_height = 100, 100
            gap = 50  # Gap between buttons
            total_width = 2 * button_width + gap  # Total width of both buttons and the gap
            x_start = (640 - total_width) / 2  # Starting x-coordinate for the buttons
            x_sub, y_sub = x_start, 480/2 - 50  # "-" button parameters
            x_add, y_add = x_start + button_width + gap, 480/2 - 50  # "+" button parameters

            # "start" button parameters
            x_start_button = x_sub
            y_start_button = 480/2 + 50
            start_button_width = total_width

            if x_add <= event.pos[0] <= x_add + button_width and y_add <= event.pos[1] <= y_add + button_height:  # Check if click is within "+" button
                new_player = Player(f"Player {len(players) + 1}")  # Create new player
                players.append(new_player)  # Add new player to list
                print(new_player.name)  # Print new player's name
            elif x_sub <= event.pos[0] <= x_sub + button_width and y_sub <= event.pos[1] <= y_sub + button_height:  # Check if click is within "-" button
                if players:  # Check if there are players to remove
                    removed_player = players.pop()  # Remove last player
                    print(f"Removed {removed_player.name}")  # Print removed player's name
            elif x_start_button <= event.pos[0] <= x_start_button + start_button_width and y_start_button <= event.pos[1] <= y_start_button + button_height:  # Check if click is within "start" button
                print("Start button clicked")  # Handle start button click
                start_clicked = True
    return start_clicked, players

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    players = [Player("Player 1")]

    while True:
        start_clicked, players = handle_events(players)
        if start_clicked:
            gameWindow(screen, players)  # Call gameWindow when start button is clicked
            break

        screen.fill((255, 255, 255))
        button_width, button_height = 100, 100
        gap = 50  # Gap between buttons
        total_width = 2 * button_width + gap  # Total width of both buttons and the gap
        x_start = (640 - total_width) / 2  # Starting x-coordinate for the buttons

        # Draw "-" button
        draw_button(screen, "-", x_start, 480/2 - 50, button_width, button_height, (255, 0, 0))
        # Draw "+" button
        draw_button(screen, "+", x_start + button_width + gap, 480/2 - 50, button_width, button_height, (0, 255, 0))
        # Draw "start" button
        draw_button(screen, "start", x_start, 480/2 + 50 + 10, total_width, button_height, (240, 240, 240))  # 10 is the top margin
        # Display total players above the button
        draw_player_count(screen, len(players), 640/2, 480/2 - 100)
        pygame.display.flip()

def gameWindow(screen, players):
    while True:
        next_round_clicked = False
        screen_width, screen_height = screen.get_size()
        player_width = screen_width / len(players)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            next_round_clicked = handle_next_round_button(event, 640/2 - 50, 480 - 50, 100, 50)
            for i, player in enumerate(players):
                x = i * player_width
                handle_player_info_button(event, player, x, 10, player_width)
        screen.fill((255, 255, 255))
        for i, player in enumerate(players):
            x = i * player_width
            draw_player_info(screen, player, x, 10, player_width)
        draw_total_population_and_pollution(screen, players, screen_width / 2, 480 - 100)
        # draw_button(screen, "Next", 640/2 - 50, 480 - 50, 100, 50, (240, 240, 240))
        
        # Draw a black border around the screen, leaving a 10-pixel margin at the bottom
        border_thickness = 5
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screen_width, screen_height - 10), border_thickness)
        
        pygame.display.flip()
        if next_round_clicked:
            pass

if __name__ == "__main__":
    main()