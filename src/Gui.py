"""This module contains the GUI for the game."""
import pygame
from src.Board import WIDTH, HEIGHT, COL, ROW

pygame.mixer.quit()
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TIMER = pygame.time.Clock()
FPS = 60
RADIUS = 15 # sprite radius
DIAMETER = 2 * RADIUS

player_image = pygame.transform.scale(pygame.image.load('assets/pac.png'), (DIAMETER, DIAMETER))
aggro_image = pygame.transform.scale(pygame.image.load('assets/ghost1.png'), (DIAMETER, DIAMETER))
dumb_image = pygame.transform.scale(pygame.image.load('assets/ghost2.png'), (DIAMETER, DIAMETER))
pattern_image = pygame.transform.scale(pygame.image.load('assets/ghost3.png'), (DIAMETER, DIAMETER))
pattern2_image = pygame.transform.scale(pygame.image.load('assets/ghost3b.png'), (DIAMETER, DIAMETER))
frightened_image = pygame.transform.scale(pygame.image.load('assets/ghost4.png'), (DIAMETER, DIAMETER))

def display_header():
    """This function displays the header of the game."""
    yellow = (255, 255, 0)

    text_font = pygame.font.Font(None, 100)
    text_surface = text_font.render("Pac-Man level", True, yellow)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 850))
    SCREEN.blit(text_surface, text_rect)

    pygame.display.update()

def display_theme_choice():
    """This function displays the theme choice screen and returns the button positions and sizes."""

    blue = (0, 0, 255)
    red = (255, 0, 0)
    purple = (128, 0, 128)

    # defining the button positions and sizes
    button_width = WIDTH // 3
    button_height = HEIGHT // 10
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 - button_height // 2

    text_font = pygame.font.Font(None, 30)
    text_surface = text_font.render("Choose color theme:", True, 'white')
    text_rect = text_surface.get_rect(center=(WIDTH // 2, button_y - 30))
    SCREEN.blit(text_surface, text_rect)

    pygame.draw.rect(SCREEN, blue, (button_x, button_y, button_width // 3, button_height))
    pygame.draw.rect(SCREEN, red, (button_x + button_width // 3, button_y, button_width // 3, button_height))
    pygame.draw.rect(SCREEN, purple, (button_x + 2 * button_width // 3, button_y, button_width // 3, button_height))

    pygame.display.update()

    return button_x, button_y, button_height, button_width

def handle_theme_choice(theme):
    """This function handles the theme choice screen and returns the chosen theme."""
    button_x, button_y, button_height, button_width = display_theme_choice()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    if mouse_x <= button_x + button_width // 3:
                        running = False
                        theme = 'blue'
                    elif mouse_x <= button_x + 2 * button_width // 3:
                        running = False
                        theme = 'red'
                    else:
                        running = False
                        theme = 'purple'
    return theme

def display_game_over(game_over_text, restart, running):
    """This function displays the game over screen and returns the restart and running variables."""
    SCREEN.fill((0, 0, 0))
    text_width = game_over_text.get_width()
    text_height = game_over_text.get_height()
    text_x = (WIDTH - text_width) // 2
    text_y = (HEIGHT - text_height) // 2
    SCREEN.blit(game_over_text, (text_x, text_y))
    pygame.display.update()

    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                restart = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart = True
    return restart, running

def display_player(x, y, direction):
    """This function displays the player image."""
    if direction == 0:
        SCREEN.blit(player_image, (x, y))
    elif direction == 1:
        SCREEN.blit(pygame.transform.flip(player_image, True, False), (x, y))
    elif direction == 2:
        SCREEN.blit(pygame.transform.rotate(player_image, 90), (x, y))
    elif direction == 3:
        SCREEN.blit(pygame.transform.rotate(player_image, 270), (x, y))

def display_ghost(x, y, image, power_up):
    """This function displays the needed ghost image."""
    if not power_up:
        SCREEN.blit(image, (x, y))
    else:
        SCREEN.blit(frightened_image, (x, y))

def display_board(coins, theme, level):
    """This function displays the board and returns the number of coins."""
    for i, block in enumerate(level):
        for j, cell in enumerate(block):
            if cell == '.':
                pygame.draw.circle(SCREEN, 'white', (j * COL + COL * 0.5, i * ROW + ROW * 0.5), 3)
                coins += 1
            elif cell == '*':
                pygame.draw.circle(SCREEN, 'yellow', (j * COL + COL * 0.5, i * ROW + ROW * 0.5), 10)
            elif cell == '#':
                pygame.draw.rect(SCREEN, theme, (j * COL, i * ROW, COL - 1, ROW - 1))
            elif cell in ('<', '>'):
                pygame.draw.circle(SCREEN, 'cyan', (j * COL + COL * 0.5, i * ROW + ROW * 0.5), 10)
            elif cell == 'o':
                pygame.draw.circle(SCREEN, 'green', (j * COL + COL * 0.5, i * ROW + ROW * 0.5), 10)
                pygame.draw.circle(SCREEN, 'black', (j * COL + COL * 0.5, i * ROW + ROW * 0.5), 5)
    return coins
