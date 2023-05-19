from rest_framework import serializers
from django.contrib.auth.models import User

from map.serializers import PlayerSerializer


class UserSerializer(serializers.ModelSerializer):
    #profiles = PlayerSerializer(read_only=True, many=True, allow_empty=True, required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'player_set')