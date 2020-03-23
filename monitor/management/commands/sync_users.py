from django.contrib.auth.models import User

from monitor.models import Site_User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            print(user.username)
            if user.has_site_user() is False:
                site_user = Site_User(user=user,
                                      location="Cluj-Napoca",first_name=user.username)
                site_user.save()
