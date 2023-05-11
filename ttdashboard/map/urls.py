from django.urls import path, register_converter
from map import views
import map

class UserIdConverter:
    """This converter will accept either an int or @me"""
    regex = "(\d+|@me)"

    def to_python(self, value):
        return int(value) if value != "@me" else "@me"

    def to_url(self, value):
        return value

register_converter(UserIdConverter, "id")

urlpatterns = [
    path('api/guild/<int:guild_id>', views.get_game),
    path('api/guild/<int:guild_id>/players', views.PlayerList.as_view()),
    path('api/guild/<int:guild_id>/players/<id:player_id>/', views.playerDetail.as_view()),
    path('api/guild/<int:guild_id>/players/<id:player_id>/move', views.move_player),
    path('api/guild/<int:guild_id>/players/<id:player_id>/attack', views.attack_player),
    path('api/guild/<int:guild_id>/players/<id:player_id>/transfer', views.transfer_player),
    path('api/guild/<int:guild_id>/players/<id:player_id>/upgrade', views.upgrade_player),
    path('api/guild/<int:guild_id>/players/<id:player_id>/vote', views.vote_player),
    path('api/guild/<int:guild_id>/create', views.create_game),
    path('api/guild/<int:guild_id>/players/create', views.add_player),
    path('guild/<int:guild_id>', views.public_map),
    path('map/guild/<int:guild_id>', views.private_map),
    path('', views.redirect_map)
]
