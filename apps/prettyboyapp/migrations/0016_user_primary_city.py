# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0015_auto_20180702_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='primary_city',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]