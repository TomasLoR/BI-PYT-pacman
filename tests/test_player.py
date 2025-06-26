"""This module contains the tests for the Player class."""
from src.Board import board
from src.Game import pacman, spawn_player
# player module is imported from Game.py

def test_player_negative_move():
    """This function tests if the player wont change its position if it hits a wall."""
    up = 2
    pacman.set_direction(up)
    tunrs_allowed = pacman.check_turns(board)
    assert not tunrs_allowed[up]
    pacman.move(board)
    assert pacman.get_pos() == (spawn_player)

def test_player_positive_move():
    """This function tests if the player will change its position if possible."""
    right = 0
    pacman.set_direction(right)
    tunrs_allowed = pacman.check_turns(board)
    assert tunrs_allowed[0]
    pacman.move(board)
    assert pacman.get_pos() != (spawn_player)

def test_player_teleport():
    """This function tests if the player will teleport to the other side of the board."""
    pacman.teleport(50)
    assert pacman.get_pos()[0] == 50

def test_player_respawn_():
    """This function tests if the player will respawn correctly."""
    pacman.move(board)
    pacman.set_direction(2)
    pacman.respawn()
    assert pacman.get_direction() == 0
    assert pacman.get_pos() == (spawn_player)
    assert pacman.get_lives() == 2
