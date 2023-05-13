from channels.staticfiles import Http404
from rest_framework import permissions

from django.http import HttpRequest, Http404

from rest_framework.generics import QuerySet

from map.models import Player, Game


class SelfOrAdmin(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view):
        player_id = view.kwargs.get("player_id")
        if player_id is None:
            raise Exception("SelfOrAdmin permission used with a view with no player_id")
        
        print(request.user)
        if request.user.is_superuser:
            return True
        if player_id == "@me":
            return True
        return False


class SafeAndAuth(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view):
        return request.method in permissions.SAFE_METHODS and request.user is not None

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view):
        return request.user.has_perm("api_admin")