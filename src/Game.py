"""This module handles the whole game and its components."""
import copy
from src.Board import board, ROW, COL, WIDTH, HEIGHT
from src.Gui import pygame, SCREEN, TIMER, FPS, RADIUS, player_image, aggro_image, dumb_image, pattern_image, pattern2_image, display_header, handle_theme_choice, display_game_over, display_board
from src.Ghost import Ghost
from src.Player import Player

# map design
level = copy.deepcopy(board)
theme = 'blue'

# game related information
coins = 0
restart = False
score = 0
power_up = False
power_count = 600
dumb_phase = 120

# player initialization
spawn_player = (WIDTH - 450, HEIGHT - 280)
player_info = {'speed': 2, 'direction': 0, 'lives': 3, 'image': player_image}
pacman = Player(spawn_player[0], spawn_player[1], player_info.copy())

# ghosts inictialization
spawn_aggro = (WIDTH - 840, HEIGHT - 894)
spawn_dumb = (WIDTH - 88, HEIGHT - 894)
spawn_pattern = (WIDTH - 240, HEIGHT - 200)
spawn_pattern2 = (WIDTH - 690, HEIGHT - 200)
ghost_info = {'speed': 2, 'direction': 3, 'stuck': False, 'image': aggro_image}
aggro = Ghost(spawn_aggro[0], spawn_aggro[1], ghost_info.copy())
ghost_info['image'] = dumb_image
dumb = Ghost(spawn_dumb[0], spawn_dumb[1], ghost_info.copy())
ghost_info['image'] = pattern_image
pattern = Ghost(spawn_pattern[0], spawn_pattern[1], ghost_info.copy())
ghost_info['image'] = pattern2_image
pattern2 = Ghost(spawn_pattern2[0], spawn_pattern2[1], ghost_info.copy())

def display_map(coins_, theme_):
    """This function calls GUI function to display the board and return the number of coins left."""
    return display_board(coins_, theme_, level)

def display_entities():
    """This function displays the entities."""
    pacman.display()
    aggro.display(power_up)
    dumb.display(power_up)
    pattern.display(power_up)
    pattern2.display(power_up)

def check_bonus(score_, power_up_, power_count_, center):
    """This function checks if the player has eaten a bonus and returns the updated score, power_up and power_count."""
    pos1 = center[0] // COL
    pos2 = center[1] // ROW
    player_x = center[0] - RADIUS
    if level[pos2][pos1] == '.':
        level[pos2][pos1] = ' '
        score_ += 1
    elif level[pos2][pos1] == '*':
        level[pos2][pos1] = ' '
        score_ += 5
        power_up_ = True
        power_count_ = 600
    elif level[pos2][pos1] == '<':
        player_x = WIDTH - 80
    elif level[pos2][pos1] == '>':
        player_x = WIDTH - 850
    return score_, power_up_, power_count_, player_x

def manage_power_up(power_up_, power_count_):
    """This function manages the power_up and returns the updated power_up and power_count."""
    if power_up_:
        power_count_ -= 1
        if power_count_ == 0:
            power_up_ = False
    return power_up_, power_count_

def check_entity_collision(pac_pos_, ghost_):
    """This function checks if the player has collided with a ghost and returns True if so."""
    return abs(pac_pos_[0] - ghost_.get_pos()[0]) <= RADIUS and abs(pac_pos_[1] - ghost_.get_pos()[1]) <= RADIUS

def respawn_entities():
    """This function respawns the entities."""
    pacman.respawn()
    aggro.respawn()
    dumb.respawn()
    pattern.respawn()
    pattern2.respawn()

def display_game_info():
    """This function displays the information seen during the game."""
    small_font = pygame.font.Font(None, 30)
    score_text = small_font.render('Score: ' + str(score), True, 'white')
    SCREEN.blit(score_text, (WIDTH - 880, HEIGHT - 20))

    if power_up:
        power_text = small_font.render('Power Up: ' + str(power_count // 60), True, 'white')
        SCREEN.blit(power_text, (WIDTH - 750, HEIGHT - 20))

    lives_text = small_font.render('Lives: ' + str(pacman.get_lives()), True, 'white')
    SCREEN.blit(lives_text, (WIDTH - 90, HEIGHT - 20))

if __name__ == "__main__":

    display_header()
    theme = handle_theme_choice(theme)

    # Game loop
    running = True
    while running:
        TIMER.tick(FPS)
        SCREEN.fill('black')

        coins = display_map(coins, theme)
        display_entities()

        pacman.move(level)
        score, power_up, power_count, pacman_x = check_bonus(score, power_up, power_count, pacman.get_center())
        pacman.teleport(pacman_x)
        power_up, power_count = manage_power_up(power_up, power_count)

        if power_up:
            aggro.move_aggro(spawn_aggro[0], spawn_aggro[1], level)
            dumb.move_aggro(spawn_dumb[0], spawn_dumb[1], level)

            pac_pos = pacman.get_pos()
            ghosts = [aggro, dumb, pattern, pattern2]
            for ghost in ghosts:
                if check_entity_collision(pac_pos, ghost):
                    score += 100
                    ghost.respawn()
        else:
            pac_pos = pacman.get_pos()

            if not aggro.get_stuck():
                aggro.move_aggro(pac_pos[0], pac_pos[1], level)
            else:
                dumb_phase -= 1
                if dumb_phase <= 0:
                    aggro.set_stuck(False)
                    dumb_phase = 120
                else:
                    aggro.move_dumb(level)
            dumb.move_dumb(level)
            pattern.move_pattern(aggro.get_pos()[1], level)
            pattern2.move_pattern(aggro.get_pos()[1], level)

            ghosts = [aggro, dumb, pattern, pattern2]
            for ghost in ghosts:
                if check_entity_collision(pac_pos, ghost):
                    respawn_entities()
                    break

        display_game_info()
        if pacman.get_lives() == 0:
            game_over_text = pygame.font.Font(None, 50).render("[Game Over] Press Spacebar to Restart", True, 'red')
            restart, running = display_game_over(game_over_text, restart, running)

        elif coins == 0:
            game_over_text = pygame.font.Font(None, 50).render("[You won] Press Spacebar to Restart", True, 'green')
            restart, running = display_game_over(game_over_text, restart, running)

        else:
            coins = 0

        if restart:
            respawn_entities()
            pacman = Player(spawn_player[0], spawn_player[1], player_info.copy())
            restart = aggro_stuck = power_up = False
            power_count, dumb_phase, score, coins = 0, 0, 0, 0
            level = copy.deepcopy(board)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.set_direction(0)
                elif event.key == pygame.K_LEFT:
                    pacman.set_direction(1)
                elif event.key == pygame.K_UP:
                    pacman.set_direction(2)
                elif event.key == pygame.K_DOWN:
                    pacman.set_direction(3)

        pygame.display.update()

    pygame.quit()
