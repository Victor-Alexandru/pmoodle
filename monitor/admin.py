from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(UserGroup)
admin.site.register(UserMessage)
admin.site.register(Site_User)
admin.site.register(GroupNotification)
