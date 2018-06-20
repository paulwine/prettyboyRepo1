# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    primary_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    special = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Ride(models.Model):
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    pickup_room = models.IntegerField()
    dropoff_room = models.IntegerField()
    pickup_datetime = models.DateField()
    appointment_time = models.TimeField()
    duration = models.IntegerField()
    round_trip = models.BooleanField()
    ambulatory = models.BooleanField()
    comments = models.TextField()
    facility_number = models.CharField(max_length=255)
    accompany_number = models.CharField(max_length=255)
    accompany_name = models.CharField(max_length=255)
    approved = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    user = models.ForeignKey(User, related_name="rides")

