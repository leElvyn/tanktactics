from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.conf import settings

from django.contrib.auth.models import User

import datetime
import sys
import ballance

from auth import serializers
# Create your views here.

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_self(request: HttpRequest):
    """
    Returns the user associated with the sender. 
    ## CURRENTLY ONLY RETURNS PLAYER ASSOCIATED WITH USER
    """
    request.user
    response = serializers.UserSerializer(request.user).data
    return JsonResponse(response)

def autologin(request: HttpRequest):
    return
    if not settings.DEBUG:
        print("WHAT TF YOU'RE RUNNING THIS IN PROD")
        sys.exit(1)
    user = User.objects.get(username=request.GET["user"])
    print(user.player_set)
    login(request, user, "django.contrib.auth.backends.ModelBackend")
    print(user)
    
    response = serializers.UserSerializer(request.user).data
    return JsonResponse(response)