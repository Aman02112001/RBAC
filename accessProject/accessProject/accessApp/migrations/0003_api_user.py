# Generated by Django 4.2.3 on 2023-07-27 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accessApp', '0002_alter_customuser_role_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='api',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='apis', to=settings.AUTH_USER_MODEL),
        ),
    ]
