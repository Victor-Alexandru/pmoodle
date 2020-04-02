from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', ]


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    skill = SkillSerializer(read_only=True)

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


class UserGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserGroup
        fields = ["isTeacher", "isLearner", "user", "group"]


class GroupNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupNotification
        fields = ["message", "color", "priority", "group"]


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = ["skill", "level", "years_of_experience"]
