from django.db.models.query import QuerySet
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from map.models import Player, Game
from map.serializers import GameSerializer, PlayerSerializer
from map import tasks

import datetime

import ballance
from map.permissions import SafeAndAuth, SelfOrAdmin, IsAdmin


# Create your views here.

################### UTILS #####################


def validate_new_game(game_dict):
    if type(game_dict["max_players"]) != int:
        return False
    if type(game_dict["allowed_joining"]) != bool:
        return False
    if type(game_dict["auto_size_of_grid"]) != bool:
        return False
    if game_dict["auto_size_of_grid"] == False:
        if type(game_dict["size_of_grid_x"]) != int:
            return False
        if type(game_dict["size_of_grid_y"]) != int:
            return False
    if type(game_dict["is_action_day_1d"]) != bool:
        return False

    if game_dict["is_action_day_1d"] == False:
        if type(game_dict["AD_duration"]) != int:
            return False

    if type(game_dict["game_start_date"]) != str:
        return False

    try:
        game_dict["game_start_date"] = datetime.datetime.fromisoformat(
            game_dict["game_start_date"]
        )
    except ValueError:
        return False

    if (
        type(game_dict["commands_channel_id"]) != int
        and type(game_dict["commands_channel_id"]) != bool
    ):
        return False

    if (
        type(game_dict["game_channel_id"]) != int
        and type(game_dict["game_channel_id"]) != bool
    ):
        return False

    return True


################## VIEWS #####################

### Players

class PlayerList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, guild_id):
        game = (
            Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
        )
        if game is None:
            raise Http404
        players = game.players.all()
        serializer = PlayerSerializer(players, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_player(request: HttpRequest, guild_id, player_id):
    game = (
        Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    )
    if game is None:
        raise Http404
        ###################################### DEBUG, IT SHOULD BE THE DISCORD ID, NOT PK ######################################
    if player_id == "@me":
        player = game.players.filter(user__id=request.user.id).first()
    else:
        player = game.players.filter(discord_id=player_id).first()
    if player is None:
        raise Http404
    return player

class playerDetail(APIView):
    """We work under the assumption that player_id can be an int, the ID, or @me, yourself."""
    permission_classes = [SelfOrAdmin|SafeAndAuth]

    def get(self, request, guild_id, player_id):
        player = get_player(request, guild_id, player_id)
        serializer = PlayerSerializer(player)
        return JsonResponse(serializer.data)

    def put(self, request, guild_id, player_id):
        """pretty broken"""
        player = get_player(guild_id, player_id)
        data = request.data
        serializer = PlayerSerializer(player, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, guild_id, player_id):
        player = get_player(guild_id, player_id)
        player.delete()
        return HttpResponse(status=204)


@api_view(["POST"])
@permission_classes([IsAdmin])
def create_game(request, guild_id):
    """
    Create a new game
    Settings :
        - max_players : int
        - allowed_joining : bool
        - auto_size_of_grid : bool
        ######################## only if above is false
        - size_of_grid_x : int
        - size_of_grid_y : int
        ########################

        - is_action_day_1d : bool
        ######################## only if above is false
        - AD_duration : int
        ########################

        - game_start_date : datetime isoformat
        - commands_channel_id : int or bool # if true : create one, if false : accept everywhere
        - game_channel_id : int or bool # if true : create one, if false none
        - logs_channel_id : int or bool # if true : create one, if false none
    """
    if Game.objects.filter(guild_id=guild_id, is_ended=False).exists():
        return JsonResponse(
            {"error": "There is already a game on this guild"}, status=409
        )

    settings = request.data
    if settings is None:
        return JsonResponse({"error": "No settings provided"}, status=400)
    if not validate_new_game(settings):
        return JsonResponse({"error": "Invalid settings"}, status=400)

    if settings["game_start_date"] < datetime.datetime.utcnow():
        return JsonResponse({"error": "The game start date is before now"}, status=400)

    grid_size_x, grid_size_y = ballance.get_grid_size(settings["max_players"])

    game = Game(
        guild_id=guild_id,
        max_players=settings["max_players"],
        allowed_joining=settings["allowed_joining"],
        grid_size_x=grid_size_x,
        grid_size_y=grid_size_y,
        is_action_day_1d=settings["is_action_day_1d"],
        game_start_date=settings["game_start_date"],
        game_talk_channel=settings["commands_channel_id"],
        commands_channel=settings["game_channel_id"],
        logs_channel=settings["logs_channel_id"],
    )

    if not settings["is_action_day_1d"]:
        game.ad_duration = settings["AD_duration"]

    game.save()
    tasks.start_game(
        game.id,
        schedule=int(
            (settings["game_start_date"] - datetime.datetime.utcnow()).total_seconds()
        ),
    )
    game_response = GameSerializer(game)
    return JsonResponse(game_response.data, status=201)


@api_view(["GET"])
def get_game(request: HttpRequest, guild_id):
    game = Game.objects.filter(guild_id=guild_id).order_by("game_start_date").first()

    if not game:
        raise Http404("Game does not exist")

    serialized_game = GameSerializer(game)

    if request.user.is_authenticated:
        player_set = game.players.filter(user=request.user)
        if len(player_set) == 1: # This shouldn't ever be other than 0 or 1
            serialized_game = GameSerializer(game, player_set.first())

    json_data = serialized_game.data

    response = JsonResponse(json_data, status=200)
    json_data["guild_id"] = str(json_data["guild_id"])
    return response


@api_view(["POST"])
@permission_classes([IsAdmin])
def add_player(request, guild_id):
    """
    Create and adds a new player to the game
    Settings :
        name : str
        discord_id : long
        avatar_url : str
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game:
        raise Http404("Game does not exist")
    player_settings = request.data
    if game.is_started:
        return JsonResponse({"error": "Game already started"}, status=400)
    player = Player(
        name=player_settings["name"],
        discord_id=player_settings["discord_id"],
        avatar_url=player_settings["avatar_url"],
    )
    player.save()
    game.players.add(player)
    return JsonResponse(GameSerializer(game).data, status=201)


###################### GAME ACTIONS ######################


@api_view(["POST"])
@permission_classes([SelfOrAdmin])
def move_player(request, guild_id, player_id):
    """
    Move the player
    Settings :
        x: int
        y: int
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game.is_started:
        return JsonResponse({"error": "Game not started"}, status=400)
    player: Player = get_player(request, guild_id, player_id)
    settings = request.data
    player.move(settings["x"], settings["y"])
    return JsonResponse({"game": GameSerializer(game, player).data}, status=200)



@api_view(["POST"])
@permission_classes([SelfOrAdmin])
def attack_player(request, guild_id, player_id):
    """
    Attack the player
    Settings :
        defender_id : int
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game.is_started:
        return JsonResponse({"error": "Game not started"}, status=400)
    player: Player = get_player(request, guild_id, player_id)
    settings = request.data
    defender_player = game.players.get(id=settings["defender_id"])
    reply = player.shoot(defender_player)
    return JsonResponse(reply, status=200)



@api_view(["POST"])
@permission_classes([SelfOrAdmin])
def transfer_player(request, guild_id, player_id):
    """
    Attack the player
    Settings :
        defender_id : int
        ap_number : int
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game.is_started:
        return JsonResponse({"error": "Game not started"}, status=400)
    player: Player = get_player(request, guild_id, player_id)
    settings = request.data
    defender_player = game.players.get(id=settings["defender_id"])
    reply = player.shoot_ap(defender_player, settings["ap_number"])
    return JsonResponse(reply, status=200)



@api_view(["POST"])
@permission_classes([SelfOrAdmin])
def upgrade_player(request, guild_id, player_id):
    """
    Upgrade the player
    Settings :
        No settings
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game.is_started:
        return JsonResponse({"error": "Game not started"}, status=400)
    player: Player = get_player(request, guild_id, player_id)
    settings = request.data
    reply = player.upgrade_range()
    return JsonResponse(reply, status=200)


@api_view(["POST"])
@permission_classes([SelfOrAdmin])
def vote_player(request: HttpRequest, guild_id, player_id):
    """
    Vote for a player. Only when dead.
    Settings :
        target_id : int
    """
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game.is_started:
        return JsonResponse({"error": "Game not started"}, status=400)
    player: Player = get_player(request, guild_id, player_id)
    settings = request.data
    voted_player = game.players.get(id=settings["target_id"])
    reply = player.vote(voted_player)
    reply["game"] = GameSerializer(game, player).data
    return JsonResponse(reply, status=200)


def public_map(request, guild_id):
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game:
        context = {"message": "There is no game in this server (yet)"}
        return render(request, "map/map_error.html.dj", context)
    game_json = GameSerializer(game)
    context = {
        "guild_id": guild_id,
        "public": "true",
        "is_public": True,
        "is_focused": "false",
    }
    return render(request, "map/map_public.html.dj", context)


def private_map(request, guild_id):
    game = Game.objects.filter(guild_id=guild_id).order_by("-game_start_date").first()
    if not game:
        raise Http404("Game does not exist")
    game_json = GameSerializer(game)
    player_id = request.GET.get("focus_player_id")

    context = {
        "guild_id": guild_id,
        "public": "false",
        "is_focused": "false",
        "is_public": False,
    }
    if player_id:
        player = Player.objects.get(discord_id=player_id)
        context[
            "focus"
        ] = f'{{"x": {player.tank.x}, "y": {player.tank.y}, "range": {player.tank.range}}}'
        context["is_focused"] = "true"
    return render(request, "map/map_private.html.dj", context)


def redirect_map(request):
    return HttpResponse("Yeah")
    return redirect("/guild/613018525111549953")
