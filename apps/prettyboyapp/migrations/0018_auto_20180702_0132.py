# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0017_user_primary_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facility_pay',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='user',
            name='private_pay',
            field=models.NullBooleanField(),
        ),
    ]
