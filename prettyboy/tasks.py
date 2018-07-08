from __future__ import absolute_import, unicode_literals

import datetime 
from datetime import timedelta  
from celery import task, shared_task
from .models import User, Ride
from django.shortcuts import render, HttpResponse, redirect


@shared_task()
def task_number_one():
    

    print("SUP BITCH")
@shared_task()
def task_number_two():
     #CHECK IF RIDES HAVE PASSED AND RESCHEDULE IF THEY ARE REPEAT
    now = datetime.date.today()
    rides = Ride.objects.all()
    dateswitch = False
    for ride in rides:
        if ride.pickup_datetime < now:
            
            if ride.repeat_ride:
                new_date = (now + datetime.timedelta(days=7))
                old_id = ride.id
                ride.pk = None
                ride.save()
                new_ride = Ride.objects.last()
                new_ride.pickup_datetime = new_date
                new_ride.save()
                old_ride = Ride.objects.get(id=old_id)
                old_ride.delete()
            else:
                ride.delete()
            print("RIDE DELETED")
    print(now)
  
