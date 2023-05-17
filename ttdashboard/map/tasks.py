from background_task import background

import map

import datetime
from map import tasks
import time
from django.utils import timezone

@background()
def next_action_day(game_id):
    """Background task created on start game and repeated by Game.new_action_day()"""
    game = map.models.Game.objects.get(id=game_id)
    game.new_action_day()

@background()
def start_game(game_id):
    game = map.models.Game.objects.get(id=game_id)
    game.start_game()

