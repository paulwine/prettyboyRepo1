# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-09 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prettyboyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='appointment_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ride',
            name='appointment_time',
            field=models.TimeField(),
        ),
    ]
