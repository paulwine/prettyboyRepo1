# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-11 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0025_ride_dropoff_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='reason_for_denial_OPTIONAL',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
