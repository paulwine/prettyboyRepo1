# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-10 00:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0007_ride_accompany_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='pickup_date',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='pickup_time',
        ),
        migrations.AddField(
            model_name='ride',
            name='pickup_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
