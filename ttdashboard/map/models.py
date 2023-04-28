from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import datetime
import logging


import utils
import ballance
from map import tasks
import map

import random

# Create your models here.


class BaseEvent(models.Model):
    id = models.BigIntegerField(primary_key=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, verbose_name=_("Game"))
    date = models.DateTimeField(verbose_name=_("Date"), auto_now=True)


class MoveEvent(BaseEvent):
    player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, verbose_name=_("Player")
    )
    new_x = models.IntegerField(verbose_name=_("New X"))
    new_y = models.IntegerField(verbose_name=_("New Y"))

    old_x = models.IntegerField(verbose_name=_("Old X"))
    old_y = models.IntegerField(verbose_name=_("Old Y"))


class ShootEvent(BaseEvent):
    offensive_player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        verbose_name=_("Offensive Player"),
        related_name="offensive_player",
    )
    defensive_player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, verbose_name=_("Defensive Player")
    )

    # these are the tanks at the time of the shoot
    offensive_tank = models.ForeignKey(
        "Tank",
        on_delete=models.PROTECT,
        verbose_name=_("Tank"),
        related_name="shoot_offensive_tank",
        null=True,
    )
    defensive_tank = models.ForeignKey(
        "Tank",
        on_delete=models.PROTECT,
        verbose_name=_("Tank"),
        related_name="shoot_defensive_tank",
        null=True,
    )


class TransferEvent(BaseEvent):
    offensive_player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        verbose_name=_("Offensive Player"),
        related_name="transfer_offensive_player",
    )
    defensive_player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, verbose_name=_("Defensive Player")
    )

    # these are the tanks at the time of the shoot
    offensive_tank = models.ForeignKey(
        "Tank",
        on_delete=models.PROTECT,
        verbose_name=_("Tank"),
        related_name="transfer_offensive_tank",
        null=True,
    )
    defensive_tank = models.ForeignKey(
        "Tank",
        on_delete=models.PROTECT,
        verbose_name=_("Tank"),
        related_name="transfer_defensive_tank",
        null=True,
    )


class RangeUpgradeEvent(BaseEvent):
    player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, verbose_name=_("Player")
    )
    new_range = models.IntegerField(verbose_name=_("New Range"))


class Player(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    discord_id = models.BigIntegerField(verbose_name=_("Discord ID"))
    avatar_url = models.URLField(verbose_name=_("Avatar URL"))

    is_dead = models.BooleanField(verbose_name=_("Is dead?"), default=False)
    ad_vote = models.ForeignKey(
        "Player",
        on_delete=models.SET_NULL,
        verbose_name=_("Daily Vote for this dead player"),
        null=True,
        blank=True,
    )  # If the player is dead, vote for the curent action day

    player_color = models.CharField(
        _("Player's color, in format 'rgb(x, x, x)'"), max_length=18
    )

    def move(self, x, y):
        position_x = self.tank.x
        position_y = self.tank.y

        if self.is_dead:
            raise Exception(_("Player is dead"))

        if abs(position_x - x) != 1 and abs(position_y - y) != 1:
            raise Exception(_("Player is either not moving or moving more than 1 tile"))

        game_object = self.game_set.all().first()

        if abs(x) > game_object.grid_size_x or abs(y) > game_object.grid_size_y:
            raise Exception(_("Player is outside the map"))

        if (
            game_object.players.filter(tank__x=position_x, tank__y=position_y).count()
            > 1
        ):
            # the 1 is you
            raise Exception(_("Player is in another players position"))

        if self.tank.action_points <= 0:
            raise Exception(_("Player does not have enough action points"))

        MoveEvent.objects.create(
            player=self,
            game=game_object,
            new_x=x,
            new_y=y,
            old_x=self.tank.x,
            old_y=self.tank.y,
        )

        self.tank.action_points -= 1
        self.tank.x = x
        self.tank.y = y
        self.tank.save()
        self.save()

        broadcast_event(
            game_object,
            "move",
            {
                "position": {"x": position_x, "y": position_y},
                "direction": {"x": x - position_x, "y": y - position_y},
                "player": map.serializers.PlayerSerializer(self).data,
            },
        )

    def shoot(self, defensive_player):
        reply = {"defensive_player_dead": False}

        if self.is_dead or defensive_player.is_dead:
            raise Exception(_("Player is dead"))

        if self.tank.action_points <= 0:
            raise Exception(_("Player does not have enough action points"))

        if utils.math.get_distance(self.tank, defensive_player.tank) > self.tank.range:
            raise Exception(_("Player is not in range"))

        self.tank.action_points -= 1

        defensive_player.tank.health_points -= 1
        reply["defender_health"] = defensive_player.tank.health_points
        if defensive_player.tank.health_points <= 0:
            defensive_player.is_dead = True
            reaming_tanks = self.game_set.all().first().players.filter(is_dead=False)
            if reaming_tanks.count() == 1:
                self.game_set.all().first().finish_game()
            reply["defensive_player_dead"] = True

        event = ShootEvent.objects.create(
            game=self.game_set.first(),
            offensive_player=self,
            defensive_player=defensive_player,
            offensive_tank=self.tank,
            defensive_tank=defensive_player.tank,
        )
        event.save()

        self.tank.save()
        defensive_player.tank.save()
        defensive_player.save()
        self.save()
        broadcast_event(
            self.game_set.all().first(),
            "shoot",
            {
                "offensive_player": map.serializers.PlayerSerializer(self).data,
                "defensive_player": map.serializers.PlayerSerializer(defensive_player).data,
            },
        )

        return reply

    def shoot_ap(self, defensive_player, number_of_ap_to_shoot):
        if self.is_dead or defensive_player.is_dead:
            raise Exception(_("Player is dead"))

        if self.tank.action_points < number_of_ap_to_shoot:
            raise Exception(_("Player does not have enough action points"))

        if utils.math.get_distance(self.tank, defensive_player.tank) > self.tank.range:
            raise Exception(_("Player is not in range"))

        self.tank.action_points -= number_of_ap_to_shoot

        defensive_player.tank.action_points += number_of_ap_to_shoot

        event = TransferEvent(
            game=self.game_set.first(),
            offensive_player=self,
            defensive_player=defensive_player,
            offensive_tank=self.tank,
            defensive_tank=defensive_player.tank,
        )
        event.save()
        defensive_player.tank.save()
        self.tank.save()

        defensive_player.save()
        self.save()
        reply = {
            "new_offender_ap": self.tank.action_points,
            "new_defender_ap": defensive_player.tank.action_points,
        }
        
        broadcast_event(
            self.game_set.all().first(),
            "upgrade",
            {
                "player": map.serializers.PlayerSerializer(self).data,
                "new_range": self.tank.range
            },
        )
        return reply

    def upgrade_range(self):
        upgrade_cost = self.tank.range - 1
        if self.tank.action_points < upgrade_cost:
            raise Exception(_("Player does not have enough action points"))
        self.tank.action_points -= upgrade_cost
        self.tank.range += 1
        event = RangeUpgradeEvent(
            game=self.game_set.first(), player=self, new_range=self.tank.range
        )
        event.save()
        self.tank.save()

        broadcast_event(
            self.game_set.all().first(),
            "upgrade",
            {
                "player": map.serializers.PlayerSerializer(self).data,
                "new_range": self.tank.range
            },
        )

        reply = {"new_range": self.tank.range}
        return reply

    def vote(self, player):
        """send the vote of this dead player to player. If player has 3 votes, he gets an ation_point"""
        if not self.is_dead:
            raise Exception(_("Player is not dead"))

        if self.ad_vote is not None:
            raise Exception(_("Player already voted"))

        self.ad_vote = player
        self.save()
        if Player.objects.filter(ad_vote=player).count() == 3:
            player.tank.action_points += 1
            player.tank.save()
        self.save()
        player.save()
        reply = {"vote_number": Player.objects.filter(ad_vote=player).count()}
        return reply

    def __str__(self):
        return self.name


class Tank(models.Model):
    id = models.BigIntegerField(primary_key=True)
    player = models.OneToOneField(
        Player, on_delete=models.PROTECT, verbose_name=_("Player"), null=True
    )

    action_points = models.IntegerField(verbose_name=_("Action points"), default=1)
    health_points = models.IntegerField(verbose_name=_("Health points"), default=3)
    range = models.IntegerField(verbose_name=_("Range"), default=2)

    x = models.IntegerField(verbose_name=_("Position X"), default=0)
    y = models.IntegerField(default=0, verbose_name=_("Position Y"))

    def __str__(self):
        return str(self.player)


class Game(models.Model):
    id = models.BigIntegerField(primary_key=True)
    guild_id = models.BigIntegerField(verbose_name=_("Guild ID"))
    players = models.ManyToManyField(
        Player,
        verbose_name=_("Player List"),
    )
    allowed_joining = models.BooleanField(
        verbose_name=_("Is everyone allowed to join ?")
    )
    max_players = models.IntegerField(verbose_name=_("Max players"))

    game_talk_channel = models.BigIntegerField(
        verbose_name=_("Game discussions channel ID")
    )
    commands_channel = models.BigIntegerField(verbose_name=_("Commands channel ID"))
    logs_channel = models.BigIntegerField(verbose_name=_("Logs channel ID"))

    # size from the middle to border
    grid_size_x = models.IntegerField(verbose_name=_("Grid size X"))
    grid_size_y = models.IntegerField(verbose_name=_("Grid size Y"))

    is_action_day_1d = models.BooleanField(
        verbose_name=_("Is an Action Day lasting 1 day ?")
    )
    ad_duration = models.IntegerField(
        verbose_name=_("Duration of the AD in minutes"),
        default=datetime.timedelta(days=1).total_seconds() / 60,
    )

    is_started = models.BooleanField(
        verbose_name=_("Is the game started ?"), default=False
    )
    is_ended = models.BooleanField(verbose_name=_("Is the game ended ?"), default=False)

    next_ad_end = models.DateTimeField(verbose_name=_("Next AD end"), null=True)

    game_start_date = models.DateTimeField(verbose_name=_("Game start"))

    def new_action_day(self):
        self.next_ad_end += datetime.timedelta(minutes=self.ad_duration)
        for player in self.players.all():
            if player.is_dead:
                player.ad_vote = None
            else:
                player.tank.action_points += 1
                player.tank.save()
            player.save()
        self.save()

    def start_game(self):
        self.is_started = True
        self.save()
        self.next_ad_end = self.game_start_date + datetime.timedelta(
            seconds=self.ad_duration
        )

        grid_size_x, grid_size_y = ballance.get_grid_size(self.players.count())
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        for player in self.players.all():
            tank = Tank(
                player=player,
                x=random.randint(0, grid_size_x),
                y=random.randint(0, grid_size_y),
            )
            tank.save()
            tank.save()
            player.player_color = f"rgb({random.randint(50, 190)}, {random.randint(50, 190)}, {random.randint(50, 190)})"
            player.save()
        self.save()

    def finish_game(self):
        self.is_ended = True


def broadcast_event(game: Game, event_type, data):
    layer = get_channel_layer()
    # Send message to room group
    game_serialized = map.serializers.GameSerializer(game)
    print(game.guild_id)
    async_to_sync(layer.group_send)(
        f"game_{game.guild_id}",
        {"type": event_type, "data": data, "new_game_data": game_serialized.data},
    )


@receiver(pre_save)
def pre_save_set_snowflake_id(sender, instance, *args, **kwargs):
    """
    Django Signals, pre_save
    //Applicable to all model s
    If we dont include the sender argument in the decorator,
    like @receiver(pre_save, sender=MyModel), the callback will be called for all models.
    """
    # print(__name__)  # = polls.models
    # print(type(instance)) # = <class 'polls.models.Question'>
    if __name__ in str(type(instance)) and not instance.id:
        # Meet the conditions (1) in this models.py The model whose model (2) id declared in is not empty will use snowflake to generate ID
        # The reason is that if you do not add conditions (1), it will be like auth_ Table at the beginning and django_ The starting table will also use the id generated by snowflake, but its id length is not enough.
        instance.id = utils.snowflakes.snowflake(instance, instance.id)
