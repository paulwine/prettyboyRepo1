from __future__ import absolute_import, unicode_literals

import datetime 
from datetime import timedelta  
from celery import task
from .models import User, Ride, PastRide
from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

@task()
def task_number_one():
    rides = Ride.objects.all()
    for ride in rides:
        if ride.pending:
            if ride.approved == None:
                ride.pending = True
                ride.save()
            else:
                if ride.approved == True:
                    #Send email to client and remove from pending rides in session
                    ride.pending = False
                    body = "Ride Approved!"
                    trip_txt = ""
                    if ride.round_trip:
                        trip_txt = "Round Trip"
                    else:
                        trip_txt = "One Way"
                    
                    current_user = ride.user

                    msg_html = render_to_string('confirm_email.html', {
                        'rider_first': current_user.first_name,
                    
                        'date': ride.pickup_datetime,
                        'time' : ride.appointment_time,
                        'pickup' : ride.pickup_address,
                        'dropoff' : ride.dropoff_address,
                        'round_trip': trip_txt
                        })
                    
                    
                    
                    send_mail(
                        'Papuga: Ride Approved!',
                        body,
                        'paulwinegard@gmail.com',
                        [current_user.email],
                        fail_silently=False,
                        html_message=msg_html,
                    )
                    ride.save()
                else:
                    ride.pending = False
                    trip_txt = ""
                    if ride.round_trip:
                        trip_txt = "Round Trip"
                    else:
                        trip_txt = "One Way"
                    
                    current_user = ride.user
                    msg_html = render_to_string('denied_email.html', {
                        'rider_first': current_user.first_name,
                    
                        'date': ride.pickup_datetime,
                        'time' : ride.appointment_time,
                        'pickup' : ride.pickup_address,
                        'dropoff' : ride.dropoff_address,
                        'round_trip': trip_txt
                        })
                    
                    body = "Ride Denied"
                    
                    send_mail(
                        'Papuga: Ride Denied',
                        body,
                        'paulwinegard@gmail.com',
                        [current_user.email],
                        fail_silently=False,
                        html_message=msg_html,
                    )
                    ride.save()
                    #Send email to reschedule for client and remove from pending rides in session.
            
            
    
    
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
                new_ride = Ride.objects.create(dropoff_number = ride.dropoff_number, doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= new_date, appointment_time= ride.appointment_time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
                new_past_ride = PastRide.objects.create(dropoff_number = ride.dropoff_number,doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= ride.pickup_datetime, appointment_time= ride.appointment_time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
                ride.delete()
                print("RIDE RESCHEDULED")
            else:    
                ride.delete()
                print("RIDE DELETED")
    print(now)
  
@task()
def task_number_three():
    past_rides = PastRide.objects.all()

    if len(past_rides) > 30:
        PastRide.objects.first.delete()
        
