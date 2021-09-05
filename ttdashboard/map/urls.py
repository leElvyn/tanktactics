from django.urls import path
from map import views
import map

urlpatterns = [
    path('api/guild/<int:guild_id>', views.get_game),
    path('api/guild/<int:guild_id>/players', views.PlayerList.as_view()),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/', views.playerDetail.as_view()),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/move', views.move_player),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/attack', views.attack_player),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/transfer', views.transfer_player),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/upgrade', views.upgrade_player),
    path('api/guild/<int:guild_id>/players/<int:discord_id>/vote', views.vote_player),
    path('api/guild/<int:guild_id>/create', views.create_game),
    path('api/guild/<int:guild_id>/players/create', views.add_player),
    path('guild/<int:guild_id>', views.public_map),
    path('map/guild/<int:guild_id>', views.private_map),
    path('', views.redirect_map)
]
