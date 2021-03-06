# Generated by Django 3.0.4 on 2020-04-04 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitor', '0008_auto_20200402_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestToGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Group')),
                ('request_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user_request', to=settings.AUTH_USER_MODEL)),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
