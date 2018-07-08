from __future__ import absolute_import, unicode_literals

import datetime 
from datetime import timedelta  
from celery import task
from .models import User, Ride, PastRide
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
            if ride.repeat_ride:
                new_date = now + datetime.timedelta(days=7)
                new_ride = Ride.objects.create(doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= new_date, appointment_time= ride.appointment_time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
                new_past_ride = PastRide.objects.create(doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= ride.pickup_datetime, appointment_time= ride.appointment_time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
                ride.delete()
                print("RIDE RESCHEDULED")
            else:    
                ride.delete()
                print("RIDE DELETED")
    print(now)
  
