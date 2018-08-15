# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-12 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0026_ride_reason_for_denial_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='additional_destination_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='additional_destination_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='additional_time_1',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='additional_time_2',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
