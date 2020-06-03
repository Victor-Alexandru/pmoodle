from django.shortcuts import render
# jwtauth/views.py

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

from monitor.models import Site_User
from .serializers import UserCreateSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    description = request.data.get("description")
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    # when the user is ready we need to create a site user
    if description:
        site_user = Site_User(user=user, first_name=user.username, description=description)
        site_user.id = user.id
        site_user.save()
    else:
        site_user = Site_User(user=user, first_name=user.username)
        site_user.id = user.id
        site_user.save()

    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)
# Create your views here.
