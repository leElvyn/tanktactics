from rest_framework import serializers
from rest_framework.fields import empty
from map.models import Player, Game, Tank

class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = ["action_points", "health_points", "x", "y", "range"]

class PlayerVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name"]

class PlayerSerializer(serializers.ModelSerializer):
    tank = TankSerializer(read_only=True)
    
    ad_vote = PlayerVoteSerializer()
    
    class Meta:
        model = Player
        fields = ["id", "name", "tank", "discord_id", "avatar_url", "is_dead", "ad_vote", "game_set", "player_color", "vote_received"]

class GameSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, self_instance: Player = None, **kwargs):
        if self_instance == None:
            self.self_data =None
            super().__init__(instance, **kwargs)
        else:
            self.self_data = PlayerSerializer(self_instance).data
            super().__init__(instance, **kwargs)

    def get_self(self, obj):
        return self.self_data

    self = serializers.SerializerMethodField()

    players = PlayerSerializer(read_only=True, many=True)
    class Meta:
        model = Game
        fields = ["id", "guild_id", "players", "allowed_joining", "max_players", "game_talk_channel", "commands_channel", "logs_channel", "grid_size_x", "grid_size_y", "is_action_day_1d", "ad_duration", "is_started", "is_ended", "next_ad_end", "game_start_date", "self"]

class EventSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        self.Meta.model = instance.__class__
        super().__init__(instance, **kwargs)

    class Meta:
        model = None