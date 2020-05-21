# Generated by Django 3.0.6 on 2020-05-12 15:51

from django.db import migrations, models
import django.utils.crypto
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=functools.partial(django.utils.crypto.get_random_string, *(20,), **{}), max_length=20, unique=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]