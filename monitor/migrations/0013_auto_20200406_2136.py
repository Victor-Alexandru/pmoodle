# Generated by Django 3.0.4 on 2020-04-06 18:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitor', '0012_auto_20200406_2132'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usergroup',
            unique_together={('user', 'group')},
        ),
    ]
