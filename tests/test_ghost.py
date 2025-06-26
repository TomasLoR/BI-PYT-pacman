"""This file contains the tests for the Ghost class."""
from src.Board import board
from src.Game import aggro, dumb, pattern, spawn_aggro, spawn_dumb, spawn_pattern

def manhattan_dist(dummy_pos, ghost_pos):
    """This is a helper function that calculates the manhattan distance between two points."""
    return abs(dummy_pos[0] - ghost_pos[0]) + abs(dummy_pos[1] - ghost_pos[1])

def test_ghosts_moves():
    """This function tests if the ghosts move correctly."""
    dummy_pos = (450, 670)
    for index, ghost in enumerate((aggro, dumb, pattern)):
        if index == 0:
            curr_distance = manhattan_dist(dummy_pos, ghost.get_pos())
            ghost.move_aggro(dummy_pos[0], dummy_pos[1], board)
            new_distance = manhattan_dist(dummy_pos, ghost.get_pos())
            assert new_distance <= curr_distance
        elif index == 1:
            ghost.move_dumb(board)
            assert (ghost.get_pos()[0] != spawn_dumb[0] or ghost.get_pos()[1] != spawn_dumb[1])
        elif index == 2:
            ghost.move_pattern(aggro.get_pos()[1], board)
            if spawn_pattern[1] > aggro.get_pos()[1]:
                assert ghost.get_pos()[1] == spawn_pattern[1] - ghost.get_speed()
            elif spawn_pattern[1] < aggro.get_pos()[1]:
                assert ghost.get_pos()[1] == spawn_pattern[1] + ghost.get_speed()

def test_ghost_respawn():
    """This function tests if the ghosts respawn correctly."""
    for index, ghost in enumerate((aggro, dumb, pattern)):
        ghost.respawn()
        if index == 0:
            assert ghost.get_pos() == (spawn_aggro[0], spawn_aggro[1])
        elif index == 1:
            assert ghost.get_pos() == (spawn_dumb[0], spawn_dumb[1])
        elif index == 2:
            assert ghost.get_pos() == (spawn_pattern[0], spawn_pattern[1])
