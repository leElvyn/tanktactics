from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor

from .models import Game, Player, Tank, MoveEvent

class TankInline(admin.TabularInline):
    model = Tank


class PlayerAdmin(admin.ModelAdmin):
    inlines = [TankInline]

    # Register your models here.
class PlayerInline(admin.TabularInline):
    model = Player.game_set.through

class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Guild informations", {'fields': ['guild_id', 'game_talk_channel', 'commands_channel', "logs_channel"]}),
        ("Players", {'fields': ['players']}),
        ("Game settings", {'fields': [ 'allowed_joining', 'max_players', 'grid_size_x', "grid_size_y", "ad_duration", "game_start_date", "is_action_day_1d"]}),
        ("Game status", {'fields': ["is_started", "is_ended", "next_ad_end"]}),
    ]
    inlines = [PlayerInline]

    
pset:ReverseManyToOneDescriptor = User.player_set

class PlayerInlineUser(admin.TabularInline):
    model = Player
    fields = ["name"]
    max_num = 0

UserAdmin.inlines = [PlayerInlineUser]

admin.site.register(MoveEvent)
admin.site.register(Game, GameAdmin)
admin.site.register(Player)
admin.site.register(Tank)
