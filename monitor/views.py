from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.exceptions import PermissionDenied
from monitor.serializers import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class GroupList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Group.objects.filter(owner=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        locality = self.request.query_params.get("locality")
        if locality:
            return User.objects.all().filter(location=locality)
        else:
            return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def perform_update(self, serializer):
        serializer.save()


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UserMessageList(generics.ListCreateAPIView):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        first_user_id = self.request.query_params.get("first_user_id")
        second_user_id = self.request.query_params.get("second_user_id")

        if first_user_id and second_user_id:
            first_user = User.objects.all().get(pk=first_user_id)
            second_user = User.objects.all().get(pk=second_user_id)

            return UserMessage.objects.all().filter(
                Q(owner=first_user, to_user_msg=second_user) | Q(owner=second_user, to_user_msg=first_user)).order_by(
                'time')

        return UserMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(time=timezone.now())


class SiteUserList(generics.ListCreateAPIView):
    serializer_class = SiteUserSerializer

    def get_queryset(self):
        locality = self.request.query_params.get("locality")
        if locality:
            return Site_User.objects.all().filter(location=locality).exclude(user=self.request.user)
        else:
            return Site_User.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class SiteUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site_User.objects.all()

    serializer_class = SiteUserSerializer

    def perform_update(self, serializer):
        serializer.save()
