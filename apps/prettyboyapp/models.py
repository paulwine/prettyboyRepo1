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
    primary_facility_name = models.CharField(max_length=255)
    primary_facility_address = models.CharField(max_length=255)
    primary_facility_number = models.CharField(max_length=255)
    primary_city = models.CharField(max_length=255)
    primary_room_number = models.CharField(max_length=255)
    private_pay = models.NullBooleanField(null=True)
    facility_pay = models.NullBooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

    def __unicode__(self):
       return self.first_name + " " + self.last_name

class Ride(models.Model):
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    dropoff_number = models.CharField(max_length=255)
    pickup_room = models.IntegerField()
    dropoff_room = models.IntegerField()
    pickup_datetime = models.DateField()
    pickup_time = models.TimeField(null=True)
    appointment_time = models.TimeField()
    duration = models.CharField(max_length=255)
    round_trip = models.BooleanField()
    ambulatory = models.BooleanField()
    doctor_name = models.CharField(max_length=255)
    doctor_suite_number = models.CharField(max_length=255)
    doctor_office_number = models.CharField(max_length=255)
    comments = models.TextField()
    facility_number = models.CharField(max_length=255)
    accompany_number = models.CharField(max_length=255)
    accompany_name = models.CharField(max_length=255)
    approved = models.NullBooleanField(null=True)
    reason_for_denial_OPTIONAL = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    repeat_ride = models.BooleanField()

    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    pending = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name="rides", on_delete=models.CASCADE)

class PastRide(models.Model):
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    pickup_room = models.IntegerField()
    dropoff_room = models.IntegerField()
    dropoff_number = models.CharField(max_length=255)
    pickup_datetime = models.DateField()
    pickup_time = models.TimeField(null=True)
    appointment_time = models.TimeField()
    duration = models.CharField(max_length=255)
    round_trip = models.BooleanField()
    ambulatory = models.BooleanField()
    doctor_name = models.CharField(max_length=255)
    doctor_suite_number = models.CharField(max_length=255)
    doctor_office_number = models.CharField(max_length=255)
    comments = models.TextField()
    facility_number = models.CharField(max_length=255)
    accompany_number = models.CharField(max_length=255)
    accompany_name = models.CharField(max_length=255)
    approved = models.NullBooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    repeat_ride = models.BooleanField()

    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()



    user = models.ForeignKey(User, related_name="past_rides", on_delete=models.CASCADE)
   
