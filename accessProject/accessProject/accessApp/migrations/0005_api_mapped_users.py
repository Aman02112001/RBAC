# Generated by Django 4.2.3 on 2023-07-31 10:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessApp', '0004_alter_api_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='api',
            name='mapped_users',
            field=models.ManyToManyField(blank=True, related_name='mapped_apis', to=settings.AUTH_USER_MODEL),
        ),
    ]
