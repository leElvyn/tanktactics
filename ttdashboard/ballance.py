import math

"""this file contain every ballance variables and method for the game."""

def get_grid_size(number_of_players):
    number_of_players *= 18
    return (math.ceil(math.sqrt(number_of_players)) + 7, math.ceil(math.sqrt(number_of_players)) + 7)