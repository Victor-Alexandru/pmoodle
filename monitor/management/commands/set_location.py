from monitor.models import Site_User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('location', type=str, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        location = kwargs['location']
        for user in Site_User.objects.all():
            user.location = location
            user.save()

