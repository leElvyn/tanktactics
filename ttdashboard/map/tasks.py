from background_task import background

import map

import datetime
from map import tasks
import time
from django.utils import timezone

@background(schedule=5)
def check_action_day():
    current_games = map.models.Game.objects.filter(is_started=True, is_ended=False)
    for game in current_games:
        if not game.next_ad_end:
            return # THIS IS FOR TESTING IN CASE THE START GAME FAILS

        if game.next_ad_end.timestamp() < datetime.datetime.utcnow().timestamp():
            game.new_action_day()

@background()
def start_game(game_id):
    game = map.models.Game.objects.get(id=game_id)
    game.start_game()

