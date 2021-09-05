from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_sf>\w+)/$', consumers.ClientConsumer.as_asgi()),
]
