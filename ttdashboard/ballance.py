import math

"""this file contain every ballance variables and method for the game."""

def get_grid_size(number_of_players):
    number_of_players *= 24 #the idea is that every player takes about 24 squares of space
    return (math.ceil(math.sqrt(number_of_players)), math.ceil(math.sqrt(number_of_players)))