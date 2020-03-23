from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', ]


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Group
        fields = ['id', 'name', 'group_size', 'estimated_work_duration', 'owner', 'skill']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'isVideo', 'isMessage', 'message', 'background_color', ]


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'aim_for_survey', ]


class EvaluationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationSession
        fields = ['id', 'start_date', 'end_date', 'name', ]


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ['id', 'text', 'points', 'type', ]


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['id', 'text', 'to_user_msg', 'time']


class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site_User
        fields = ['id', 'location', 'user', 'first_name']
