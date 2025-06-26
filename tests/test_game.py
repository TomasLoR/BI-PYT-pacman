"""This module contains the tests for the game module."""
from src.Board import board, ROW, COL
from src.Game import manage_power_up, check_bonus, check_entity_collision, aggro

def test_manage_power_up():
    """This function tests if the power up manager is working correctly."""
    power_up = True
    power_count = 2
    power_up, power_count = manage_power_up(power_up, power_count)
    assert power_up and power_count == 1
    power_up, power_count = manage_power_up(power_up, power_count)
    assert not power_up and power_count == 0

def test_check_bonus():
    """This function tests if the check_bonus function is detecting all the bonuses."""
    coins = 0
    cherry = 0
    for i, block in enumerate(board):
        for j, cell in enumerate(block):
            if cell == '.':
                coins_ = coins
                coins = check_bonus(coins_, False, 0, (j * COL + 15, i * ROW + 15))[0]
                assert coins == coins_ + 1
            elif cell == '*':
                cherry_ = cherry
                power_up = False
                power_count = 0
                cherry, power_up, power_count, _ = check_bonus(cherry_, power_up, power_count, (j * COL + 15, i * ROW + 15))
                assert cherry == cherry_ + 5 and power_up and power_count == 600
            elif cell in ('<', '>'):
                player_x = check_bonus(0, False, 0, (j * COL + 15, i * ROW + 15))[3]
                if cell == '<':
                    assert player_x == 820
                else:
                    assert player_x == 50

def test_check_entity_collision():
    """This function tests if the entity collision is detected correctly."""
    pac_pos = (450, 670)
    assert not check_entity_collision(pac_pos, aggro)
    for x in range(pac_pos[0] - 15, pac_pos[0] + 16, 15):
        for y in range(pac_pos[1] - 15, pac_pos[1] + 16, 15):
            aggro.set_pos(x, y)
            assert check_entity_collision(pac_pos, aggro)
