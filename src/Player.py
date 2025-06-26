"""This module contains the Player class and its methods."""""
from src.Board import ROW, COL
from src.Gui import RADIUS, display_player

class Player:
    """This class represents a single player and its abilities."""
    def __init__(self, x, y, player_info):
        self.spawn_x = self.x = x
        self.spawn_y = self.y = y
        self.player_info = player_info
        self.center_x = self.x + RADIUS
        self.center_y = self.y + RADIUS

    def display(self):
        """This method calls GUI method to display player."""
        display_player(self.x, self.y, self.player_info['direction'])

    def check_turns(self, level):
        """This method checks if the player can turn and returns the possible turns."""
        turns_allowed = [True, True, True, True]

        # wiggle room for turns
        if (self.center_x % COL) < 11 or (self.center_x % COL) > 19:
            turns_allowed[3] = False
            turns_allowed[2] = False
        else:
            if level[(self.center_y + RADIUS) // ROW][self.center_x // COL] in ('#', 'o'):
                turns_allowed[3] = False
            if level[(self.center_y - RADIUS) // ROW][self.center_x // COL] in ('#', 'o'):
                turns_allowed[2] = False

        if (self.center_y % ROW) < 11 or (self.center_y % ROW) > 19:
            turns_allowed[0] = False
            turns_allowed[1] = False
        else:
            if level[self.center_y // ROW][(self.center_x - RADIUS) // COL] in ('#', 'o'):
                turns_allowed[1] = False
            if level[self.center_y // ROW][(self.center_x + RADIUS) // COL] in ('#', 'o'):
                turns_allowed[0] = False
        return turns_allowed

    def move(self, level):
        """This method moves the player in the direction it is facing, if possible."""
        turns_allowed = self.check_turns(level)
        if self.player_info['direction'] == 0 and turns_allowed[0]:
            self.x += self.player_info['speed']
        elif self.player_info['direction'] == 1 and turns_allowed[1]:
            self.x -= self.player_info['speed']
        elif self.player_info['direction'] == 2 and turns_allowed[2]:
            self.y -= self.player_info['speed']
        elif self.player_info['direction'] == 3 and turns_allowed[3]:
            self.y += self.player_info['speed']
        self.center_x = self.x + RADIUS
        self.center_y = self.y + RADIUS

    def teleport(self, new_x):
        """This method teleports the player to the other side of the board."""
        if new_x == self.x:
            return
        self.x = new_x
        self.center_x = self.x + RADIUS

    def respawn(self):
        """This method respawns the player and updates its lives and default direction."""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.center_x = self.x + RADIUS
        self.center_y = self.y + RADIUS
        self.player_info['direction'] = 0
        self.player_info['lives'] -= 1

    def get_center(self):
        """This method returns the center coordinates of the player."""
        return (self.center_x, self.center_y)

    def get_pos(self):
        """This method returns the coordinates of the player."""
        return (self.x, self.y)

    def get_direction(self):
        """This method returns the direction of the player."""
        return self.player_info['direction']

    def get_lives(self):
        """This method returns the number of lives of the player."""
        return self.player_info['lives']

    def set_direction(self, direction):
        """This method sets the direction of the player."""
        self.player_info['direction'] = direction
