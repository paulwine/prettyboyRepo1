from __future__ import absolute_import, unicode_literals

import datetime 
from datetime import timedelta  
from celery import task
from .models import User, Ride
from django.shortcuts import render, HttpResponse, redirect

@task()
def task_number_one():
    print("SUP BITCH")
@task()
def task_number_two():
     #CHECK IF RIDES HAVE PASSED AND RESCHEDULE IF THEY ARE REPEAT
    now = datetime.date.today()
    rides = Ride.objects.all()
    dateswitch = False
    for ride in rides:
        if ride.pickup_datetime < now:
            new_ride = ride.clone()
            if ride.repeat_ride:
                new_ride.pickup_datetime  now + datetime.timedelta(days=7)

            ride.delete()
            print("RIDE DELETED")
    print(now)
  
