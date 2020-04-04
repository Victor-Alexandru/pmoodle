from django.db import models
from django.contrib.auth.models import User


def has_site_user(self):
    try:
        self.site_user
    except Exception as e:
        return False
    return True


User.add_to_class("has_site_user", has_site_user)


class Skill(models.Model):
    # TODO: enums for skills and Domain Skill
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    group_size = models.IntegerField(null=True, blank=True)
    estimated_work_duration = models.IntegerField(null=True, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING, null=False)
    owner = models.ForeignKey(User, related_name="groupings"
                              , on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    Beginner = 'BG'
    Intermiediate = 'IT'
    Expert = 'EX'
    Master = 'MS'
    LEVELS = (
        ('BG', 'Beginner'),
        ('IT', 'Intermiediate'),
        ('EX', 'Expert'),
        ('MS', 'Master'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False)
    # TODO: enums for level
    level = models.CharField(max_length=2,
                             choices=LEVELS,
                             default=Beginner, )
    years_of_experience = models.IntegerField()


class Notification(models.Model):
    isVideo = models.BooleanField(default=False)
    isMessage = models.BooleanField(default=True)
    message = models.TextField(null=True, blank=True)
    # TODO: enums for colors
    background_color = models.CharField(null=False, blank=False, max_length=250)
    # TODO: add the video for notification


class UserGroup(models.Model):  # Members table
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groupings")
    isTeacher = models.BooleanField(default=False)
    isLearner = models.BooleanField(default=True)
    start_at = models.DateField(null=True)

    class Meta:
        unique_together = (("user", "group"),)

    def __str__(self):
        return self.user.username + "  assigned to  " + self.group.name


class GroupNotification(models.Model):
    LOW = 'LW'
    MEDIUM = 'MD'
    HIGH = 'HG'
    PRIORITIES = (
        ('LW', 'LOW'),
        ('MD', 'MEDIUM'),
        ('HG', 'HIGH'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField()
    color = models.TextField()
    created_at = models.DateTimeField(null=True)
    priority = models.CharField(max_length=2,
                                choices=PRIORITIES,
                                default=LOW, )

    def __str__(self):
        return self.group.name + "  --   " + self.message


class Survey(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    aim_for_survey = models.TextField(null=True, blank=True)


class EvaluationSession(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=250, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)


class SurveyQuestion(models.Model):
    # TODO:make enum for type
    type = models.CharField(max_length=250, null=True, blank=True)
    points = models.IntegerField()
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class SurveyAnswer(models.Model):
    isValid = models.BooleanField(default=False)
    text = models.TextField()
    points_get = models.IntegerField()
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)


class UserMessage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user_msg = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    time = models.DateTimeField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)


class Site_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: enums for Location ,maybe county added
    location = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)

    # TODO: add image file

    def __str__(self):
        return self.user.username


class RequestToGroup(models.Model):
    request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_request')
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_request')
    time = models.DateTimeField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "From " + self.request_from.username + " to: " + self.request_to.username + " for group " + self.group.name
