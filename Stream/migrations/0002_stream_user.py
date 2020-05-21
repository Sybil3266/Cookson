# Generated by Django 3.0.6 on 2020-05-13 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Stream', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='user',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='stream', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]