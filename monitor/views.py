from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from monitor.serializers import *
from rest_framework import generics, status
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
    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            owner_id = self.request.query_params.get("owner_id")
            if self.request.query_params.get("owner_id"):
                return Group.objects.filter(owner=User.objects.get(pk=owner_id))
            else:
                return [ug.group for ug in UserGroup.objects.filter(user=self.request.user)] + [gr for gr in
                                                                                                Group.objects.filter(
                                                                                                    owner=self.request.user)]
        else:
            return Group.objects.all()

    def perform_create(self, serializer):
        skill_name = self.request.data.get('skill_name')
        new_skill = Skill(name=skill_name)
        new_skill.save()
        serializer.save(owner=self.request.user, skill=new_skill)


class GroupDetail(generics.RetrieveDestroyAPIView):
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
        to_user_id = self.request.query_params.get("second_user_id")

        if to_user_id:
            to_user = User.objects.all().get(pk=to_user_id)

            return UserMessage.objects.all().filter(
                Q(owner=self.request.user, to_user_msg=to_user) | Q(owner=to_user,
                                                                    to_user_msg=self.request.user)).order_by(
                'time')

        return UserMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(time=timezone.now(), owner=self.request.user)


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


class MembersList(generics.ListAPIView):
    serializer_class = SiteUserSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get("group_id")
        group_obj = get_object_or_404(Group, pk=group_id)
        if group_obj:
            users = [group_obj.owner]
            users = users + [ug.user for ug in UserGroup.objects.all().filter(group=group_obj)]

            return Site_User.objects.all().filter(user__in=users).exclude(user=self.request.user)
        else:
            return Site_User.objects.all()


class SiteUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site_User.objects.all()

    serializer_class = SiteUserSerializer

    def perform_update(self, serializer):
        serializer.save()


class UserGroupList(generics.ListCreateAPIView):
    serializer_class = UserGroupSerializer
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserGroup.objects.filter(user=user)
        else:
            return UserGroup.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, start_at=timezone.now())


class UserGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer


class GroupNotificationList(generics.ListCreateAPIView):
    serializer_class = GroupNotificationSerializer

    # permissions = (IsAuthenticated,)

    def get_queryset(self):
        group_id = self.request.query_params.get("group_id")
        if group_id:
            return GroupNotification.objects.all().filter(group=Group.objects.get(pk=group_id))
        else:
            return GroupNotification.objects.all()

    def perform_create(self, serializer):
        group = serializer.validated_data.get('group')
        if self.request.user != group.owner:
            raise Exception("Only the owner can post notifications")
        serializer.save(created_at=timezone.now())


class UserSkillList(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserSkill.objects.filter(user=self.request.user)
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer


class RequestToGroupList(generics.ListCreateAPIView):
    permissions = [IsAuthenticated, ]
    serializer_class = RequestToGroupSerializer

    def get_queryset(self):
        return RequestToGroup.objects.filter(request_to=self.request.user)

    def perform_create(self, serializer):
        group = self.request.data.get('group_id')
        if group:
            serializer.save(request_from=self.request.user, time=timezone.now(), group=Group.objects.get(pk=group))
        else:
            serializer.save(request_from=self.request.user, time=timezone.now())


class RequestToGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RequestToGroup.objects.all()
    serializer_class = RequestToGroupSerializer

    def perform_update(self, serializer):
        new_status = serializer.validated_data.get('status')
        if new_status == 'AC' and self.get_object().status == 'PG':
            ug = UserGroup(user=self.get_object().request_from, isLearner=True, isTeacher=False,
                           start_at=timezone.now(), group=self.get_object().group)
            ug.save()
            print("---------Avem UG pt request la patch ---------------")
        serializer.save()


@api_view(['GET'])
def site_user_detail(request):
    """
    Retrieve the current site-user.
    """
    if request.user.is_authenticated:
        site_user = Site_User.objects.get(user=request.user.id)

        serializer = SiteUserSerializer(site_user)

        return Response(serializer.data, status=200)
    else:
        return Response({}, status=400)
