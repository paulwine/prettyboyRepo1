# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-10 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0006_auto_20180610_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='accompany_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
