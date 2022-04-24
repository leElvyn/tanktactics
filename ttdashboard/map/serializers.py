from rest_framework import serializers
from map.models import Player, Game, Tank

class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = ["action_points", "health_points", "x", "y", "range"]

class PlayerSerializer(serializers.ModelSerializer):
    tank = TankSerializer(read_only=True)
    class Meta:
        model = Player
        fields = ["id", "name", "tank", "discord_id", "avatar_url", "is_dead", "ad_vote", "game_set", "player_color"]

class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)
    class Meta:
        model = Game
        fields = ["id", "guild_id", "players", "allowed_joining", "max_players", "game_talk_channel", "commands_channel", "logs_channel", "grid_size_x", "grid_size_y", "is_action_day_1d", "ad_duration", "is_started", "is_ended", "next_ad_end", "game_start_date"]