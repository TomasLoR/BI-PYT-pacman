"""This module contains the Ghost class and its methods."""
import random
from src.Board import ROW, COL
from src.Gui import RADIUS, display_ghost

class Ghost:
    """This class represents a single ghost and its abilities."""
    def __init__(self, x, y, ghost_info):
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.ghost_info = ghost_info
        self.center_x = self.x + RADIUS
        self.center_y = self.y + RADIUS

    def display(self, power_up):
        """This method calls GUI method to display the ghost."""
        display_ghost(self.x, self.y, self.ghost_info['image'], power_up)

    def check_turns(self, level):
        """This method checks if the ghost can turn and returns the possible turns."""
        turns_allowed = [True, True, True, True]
        self.center_x = self.x + RADIUS
        self.center_y = self.y + RADIUS

        # wiggle room for turns
        if (self.center_y % ROW) < 12 or (self.center_y % ROW) > 18:
            turns_allowed[0] = False
            turns_allowed[1] = False
        else:
            if level[self.center_y // ROW][(self.center_x + RADIUS) // COL] == '#':
                turns_allowed[0] = False
            if level[self.center_y // ROW][(self.center_x - RADIUS) // COL] == '#':
                turns_allowed[1] = False
        if (self.center_x % COL) < 12 or (self.center_x % COL) > 18:
            turns_allowed[2] = False
            turns_allowed[3] = False
        else:
            if level[(self.center_y - RADIUS) // ROW][self.center_x // COL] == '#':
                turns_allowed[2] = False
            if level[(self.center_y + RADIUS) // ROW][self.center_x // COL] == '#':
                turns_allowed[3] = False

        return turns_allowed

    def continue_move(self):
        """This method continues the previous movement of the ghost."""
        if self.ghost_info['direction'] == 0:
            self.x += self.ghost_info['speed']
        elif self.ghost_info['direction'] == 1:
            self.x -= self.ghost_info['speed']
        elif self.ghost_info['direction'] == 2:
            self.y -= self.ghost_info['speed']
        elif self.ghost_info['direction'] == 3:
            self.y += self.ghost_info['speed']

    def move_dumb(self, level):
        """This method moves the ghost randomly."""
        turns_allowed = self.check_turns(level)
        possible_moves = []

        for i in range(4):
            if turns_allowed[i]:
                if i == self.ghost_info['direction']:
                    self.continue_move()
                    return
                possible_moves.append(i)

        if len(possible_moves) > 0:
            random_direction = random.choice(possible_moves)
            if random_direction == 0:
                self.x += self.ghost_info['speed']
                self.ghost_info['direction'] = 0
            elif random_direction == 1:
                self.x -= self.ghost_info['speed']
                self.ghost_info['direction'] = 1
            elif random_direction == 2:
                self.y -= self.ghost_info['speed']
                self.ghost_info['direction'] = 2
            elif random_direction == 3:
                self.y += self.ghost_info['speed']
                self.ghost_info['direction'] = 3

    def manhattan_distance(self, new_direction, player_x, player_y):
        """This method calculates the manhattan distance between the ghost and the player and returns the distance and the new position."""
        if new_direction == 0:
            new_x = self.x + self.ghost_info['speed']
            return abs(player_x - new_x) + abs(player_y - self.y), (new_x, self.y)
        if new_direction == 1:
            new_x = self.x - self.ghost_info['speed']
            return abs(player_x - new_x) + abs(player_y - self.y), (new_x, self.y)
        if new_direction == 2:
            new_y = self.y - self.ghost_info['speed']
            return abs(player_x - self.x) + abs(player_y - new_y), (self.x, new_y)

        new_y = self.y + self.ghost_info['speed']
        return abs(player_x - self.x) + abs(player_y - new_y), (self.x, new_y)


    def move_aggro(self, player_x, player_y, level):
        """This method moves the ghost closer to the player, if possible."""
        turns_allowed = self.check_turns(level)
        self.ghost_info['stuck'] = True
        if (player_x == self.x and player_y == self.y):
            self.ghost_info['stuck'] = False
            return
        possible_moves = []
        for i in range(4):
            if turns_allowed[i]:
                possible_moves.append(i)

        if len(possible_moves) > 0:
            curr_distance = abs(player_x - self.x) + abs(player_y - self.y)
            distance_pos_list = [(curr_distance, (self.x, self.y), self.ghost_info['direction'])]
            for new_direction in possible_moves:
                distance, new_pos = self.manhattan_distance(new_direction, player_x, player_y)
                distance_pos_list.append((distance, new_pos, new_direction))
            distance_pos_list.sort(key=lambda x: x[0])
            if (self.x, self.y) != distance_pos_list[0][1]:
                self.x = distance_pos_list[0][1][0]
                self.y = distance_pos_list[0][1][1]
                self.ghost_info['direction'] = distance_pos_list[0][2]
                self.ghost_info['stuck'] = False

    def move_pattern(self, aggro_y, level):
        """This method moves the ghost according to given 'y' coordinate."""
        turns_allowed = self.check_turns(level)
        if turns_allowed[2] and aggro_y < self.y:
            self.y -= self.ghost_info['speed']
        elif turns_allowed[3] and aggro_y > self.y:
            self.y += self.ghost_info['speed']

    def respawn(self):
        """This method respawns the ghost."""
        self.x = self.spawn_x
        self.y = self.spawn_y

    def get_stuck(self):
        """This method returns the stuck attribute of the ghost."""
        return self.ghost_info['stuck']

    def set_stuck(self, stuck):
        """This method sets the stuck attribute of the ghost."""
        self.ghost_info['stuck'] = stuck

    def get_pos(self):
        """This method returns the coordinates of the ghost."""
        return (self.x, self.y)

    def set_pos(self, x, y):
        """This method sets the coordinates of the ghost."""
        self.x = x
        self.y = y

    def get_speed(self):
        """This method returns the speed of the ghost."""
        return self.ghost_info['speed']

    def set_speed(self, speed):
        """This method sets the speed of the ghost."""
        self.ghost_info['speed'] = speed
