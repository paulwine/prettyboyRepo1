# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0016_user_primary_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='primary_room_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
