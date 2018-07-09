# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from celery.schedules import crontab
from celery.task import periodic_task
from .models import User, Ride, PastRide
import datetime
import bcrypt
from dateutil import parser

  # the index function is called when root is visited
def index(request):
  if 'current_user' in request.session:
    return redirect('/welcome')
  return render(request, 'index.html')

def login(request):

  email = request.POST['email_log']
  password = request.POST['password_log']
  user_query = User.objects.filter(email=email)
  

  if len(user_query) < 1:
    messages.error(request, "Incorrect username or password")
    return redirect("/")
  else:
    hash1 = user_query[0].password
    if bcrypt.checkpw(password.encode(), hash1.encode()):
      current_user = user_query[0]
      request.session['current_user'] = current_user.id
      return redirect("/welcome")
    else:
      messages.error(request, "Incorrect username or password")
      return redirect("/")
  
  return render(request, 'login.html')

def registerpage(request):
  return render(request, 'register.html')
 
def register(request):
  error = False
  
  first = request.POST['first_name']
  last = request.POST['last_name']
  email = request.POST['email']

  # phone = request.POST['phone']
  # address = request.POST['address']
  # info = request.POST['info']

  password = request.POST['password']
  confirm_password = request.POST['confirm_password']

  user_query = User.objects.filter(email=email)
  # Validations
  if len(first) < 1 or len(last) < 1:
    messages.error(request, 'Please input a valid first and last name')
    error = True
  if len(email) < 1:
    messages.error(request, 'Email invalid.  Please input a valid email')
    error = True
  if len(password) < 8:
    messages.error(request, 'Passwords must be longer than 8 characters')
    error = True
  # if len(phone) < 1:
  #   messages.error(request, 'Please input a valid phone number')
  #   error = True
  if password != confirm_password:
    messages.error(request, 'Password do no match')
    error = True
  if len(user_query) > 0:
    messages.error(request, 'User already exists with this email address, please input a different email')
    error = True
  
  try:
    validate_email( email )
  except ValidationError:
     error = True
     messages.error(request, 'Email invalid.  Please input a valid email')


  if error == True:
    print(error)
    return redirect("/registerpage")
  else:
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print(password)
    new_user = User.objects.create(first_name=first, last_name=last, email=email, password=password)
    new_user.save()
    request.session['current_user'] = new_user.id
    return redirect("/welcome")
   
def welcome(request):
  current_user = User.objects.get(id= request.session['current_user'])
  print(current_user.first_name)
  context = {
    "user" : current_user
  }
  return render(request, 'welcome.html', context)

def contact(request):
  return render(request, "contact.html")



def schedule_ride(request):
  current_user = User.objects.get(id= request.session['current_user'])
  past_rides = PastRide.objects.filter(user=current_user)
  context = {
    "user" : current_user,
    'past_rides' : past_rides
  }
  return render(request, "schedule.html", context)

def select_past_ride(request):
  current_user = User.objects.get(id= request.session['current_user'])
  past_rides = PastRide.objects.filter(user=current_user).order_by("-pickup_datetime")[:20]
  context = {
    "user" : current_user,
    'past_rides' : past_rides
  }
  return render(request, "select_past_ride.html", context)

def schedule_ride_from_past_ride(request, rideid):
  current_user = User.objects.get(id= request.session['current_user'])
  past_ride = PastRide.objects.get(id=rideid)
  context = {
    "user" : current_user,
    'ride' : past_ride
  }
  return render(request, 'schedule_ride_from_past_ride.html', context)
def schedule_ride_from_denied_ride(request, rideid):
  current_user = User.objects.get(id= request.session['current_user'])
  denied_ride = Ride.objects.get(id=rideid)
  context = {
    "user" : current_user,
    'ride' : denied_ride
  }
  return render(request, 'schedule_ride_from_denied_ride.html', context)
def submit_past_ride(request):
  past_id = request.POST['ride_id']
  date = request.POST['date']
  time = request.POST['time']

  current_user = User.objects.get(id= request.session['current_user'])

  ride = PastRide.objects.get(id=past_id)
  new_ride = Ride.objects.create(dropoff_number = ride.dropoff_number,doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= date, appointment_time= time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
  
  trip_txt = ""
  amb_txt = ""
  if new_ride.round_trip:
    trip_txt = "Round Trip"
  else:
    trip_txt = "One Way"

  if new_ride.ambulatory:
    amb_txt = "Ambulatory"
  else:
    amb_txt = "Wheelchair Bound"  
  
  
  body = "Ride Request:"
  msg_html = render_to_string('email.html', {
    'rider_first': current_user.first_name,
    'rider_last': current_user.last_name,
    'date': new_ride.pickup_datetime,
    'time' : new_ride.appointment_time,
    'pickup' : new_ride.pickup_address,
    'dropoff' : new_ride.dropoff_address,
    'ambulatory': amb_txt,
    'round_trip': trip_txt,
    'acc_name' : new_ride.accompany_name,
    'pickup_number': new_ride.facility_number,
    'dropoff_number': new_ride.dropoff_number,
    'acc_number' : new_ride.accompany_number
    })
    
  full_name = current_user.first_name + " " + current_user.last_name
  send_mail(
    'RIDE REQUEST: {}'.format(full_name),
    body,
    'paulwinegard@gmail.com',
    ['paulwinegard@gmail.com'],
    fail_silently=False,
    html_message=msg_html,
  )

  return redirect("/manage_rides")

def submit_denied_ride(request):
  past_id = request.POST['ride_id']
  date = request.POST['date']
  time = request.POST['time']

  current_user = User.objects.get(id= request.session['current_user'])

  ride = Ride.objects.get(id=past_id)
  new_ride = Ride.objects.create(dropoff_number = ride.dropoff_number,doctor_name = ride.doctor_name, doctor_suite_number = ride.doctor_suite_number, doctor_office_number = ride.doctor_office_number, pickup_address= ride.pickup_address, pickup_datetime= date, appointment_time= time, pickup_room= ride.pickup_room, dropoff_address= ride.dropoff_address, facility_number= ride.facility_number, dropoff_room= ride.dropoff_room, duration= ride.duration, accompany_name= ride.accompany_name, accompany_number= ride.accompany_number, ambulatory= ride.ambulatory, round_trip= ride.round_trip, comments= ride.comments, user=ride.user, repeat_ride=ride.repeat_ride, monday=ride.monday, tuesday=ride.tuesday, wednesday=ride.wednesday, thursday=ride.thursday, friday=ride.friday, saturday=ride.saturday, sunday=ride.sunday)
  
  trip_txt = ""
  amb_txt = ""
  if new_ride.round_trip:
    trip_txt = "Round Trip"
  else:
    trip_txt = "One Way"

  if new_ride.ambulatory:
    amb_txt = "Ambulatory"
  else:
    amb_txt = "Wheelchair Bound"  
  
  
  body = "Ride Request:"
  msg_html = render_to_string('email.html', {
    'rider_first': current_user.first_name,
    'rider_last': current_user.last_name,
    'date': new_ride.pickup_datetime,
    'time' : new_ride.appointment_time,
    'pickup' : new_ride.pickup_address,
    'dropoff' : new_ride.dropoff_address,
    'ambulatory': amb_txt,
    'round_trip': trip_txt,
    'acc_name' : new_ride.accompany_name,
    'pickup_number': new_ride.facility_number,
    'dropoff_number': new_ride.dropoff_number,
    'acc_number' : new_ride.accompany_number
    })
    
  full_name = current_user.first_name + " " + current_user.last_name
  send_mail(
    'RIDE REQUEST: {}'.format(full_name),
    body,
    'paulwinegard@gmail.com',
    ['paulwinegard@gmail.com'],
    fail_silently=False,
    html_message=msg_html,
  )
  ride.delete()
  return redirect("/manage_rides")

def manage_rides(request):
  current_user = User.objects.get(id= request.session['current_user'])
  rides = Ride.objects.filter(user = current_user)
  context = {
    "rides" : rides
  } 
  return render(request, "manage.html", context)

def delete_ride(request, rideid):
  ride_to_delete = Ride.objects.get(id=rideid)
  ride_to_delete.delete()
  return redirect("/manage_rides")
def info(request):
  current_user = User.objects.get(id= request.session['current_user'])
  context = {
    "user" : current_user
  }
  return render(request, "info.html", context)
def save_information(request):
  current_user = User.objects.get(id= request.session['current_user'])
  current_user.first_name = request.POST['first_name']
  current_user.last_name = request.POST['last_name']
  current_user.primary_facility_name = request.POST['facility_name']
  current_user.primary_facility_address = request.POST['facility_address']
  current_user.primary_facility_number = request.POST['facility_number']
  current_user.primary_city = request.POST['primary_city']
  current_user.primary_room_number = request.POST['primary_room']

  if 'private_pay' in request.POST:
    current_user.private_pay = True
  else:
    current_user.private_pay = False
  if 'facility_pay' in request.POST:
    current_user.facility_pay = True
  else:
    current_user.facility_pay = False
  
  current_user.save()
  return redirect('/info')

def all_users(request):
  users = User.objects.all()
  print(users)
  for user in users:
    print(user.first_name + " " + user.last_name)
  return redirect("/welcome")

def submit_ride(request):
  
  error = False

  current_user = User.objects.get(id= request.session['current_user'])
  
  pickup_datetime = request.POST['pickup_datetime']
  parsed_date = parser.parse(pickup_datetime)
  print(type(pickup_datetime))
  if parsed_date < (datetime.datetime.now() + datetime.timedelta(days=1) ):
    error = True
    messages.error(request, "Rides Must Be scheduled at least 24 hours in advance")

  appointment_time = request.POST['appointment_time']
  pickup_address = request.POST['pickup_address']
  pickup_city = request.POST['pickup_city']
  pickup_full_address = pickup_address + ", " + pickup_city
  pickup_room = request.POST['pickup_room']
  pickup_phone = request.POST['pickup_number']

  dropoff_address = request.POST['dropoff_address']
  dropoff_city = request.POST['dropoff_city']
  dropoff_full_address = dropoff_address + ", " + dropoff_city
  dropoff_room = request.POST['dropoff_room']
  dropoff_number = request.POST['dropoff_phone']

  

  doctor_name =  request.POST['doctor_name']
  doctor_office_number =  request.POST['doctor_number']
  doctor_suite_number =  request.POST['doctor_room']

  accompany_name = request.POST['accompany_name']
  accompany_number = request.POST['accompany_number']
  
  ambulatory = True
  round_trip = True

  amb_txt = "Ambulatory"
  trip_txt = "Round Trip"

  if 'ambulatory' in request.POST:
    ambulatory = True
  else:
    ambulatory = False
    amb_txt = "Wheelchair Bound"

  if 'wheelchair_bound' in request.POST:
    ambulatory = False
  else:
    ambulatory = True
    amb_txt = "Ambulatory"
  
  if 'round_trip' in request.POST:
    round_trip = True
  else:
    round_trip = False
    trip_txt = "One Way"
    one_way = True

  if 'one_way' in request.POST:
    one_way = True
  else:
    one_way = False
    trip_txt = "One Way"
    round_trip = True

  duration = request.POST['duration']
  notes = request.POST['notes']

  day_array = []
  if 'repeat' in request.POST:
    repeat = True
  else:
    repeat = False

  if 'monday' in request.POST:
    monday = True
    day_array.append(0)
  else:
    monday = False

  if 'tuesday' in request.POST:
    tuesday = True
    day_array.append(1)
  else:
    tuesday = False

  if 'wednesday' in request.POST:
    wednesday = True
    day_array.append(2)
  else:
    wednesday = False

  if 'thursday' in request.POST:
    day_array.append(3)
    thursday = True
  else:
    thursday = False

  if 'friday' in request.POST:
    day_array.append(4)
    friday = True
  else:
    friday = False

  if 'saturday' in request.POST:
    day_array.append(5)
    saturday = True
  else:
    saturday = False

  if 'sunday' in request.POST:
    day_array.append(6)
    sunday = True
  else:
    sunday = False


  if error == True:
    return redirect("/schedule_ride")
  else:
    ride = Ride.objects.create(dropoff_number = dropoff_number,doctor_name = doctor_name, doctor_suite_number = doctor_suite_number, doctor_office_number = doctor_office_number, pickup_address=pickup_full_address, pickup_datetime=pickup_datetime, appointment_time= appointment_time,pickup_room=pickup_room, dropoff_address= dropoff_full_address, facility_number=dropoff_phone, dropoff_room=dropoff_room, duration= duration, accompany_name= accompany_name, accompany_number=accompany_number, ambulatory= ambulatory, round_trip=round_trip, comments=notes, user=current_user, repeat_ride=repeat, monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)
    
    current_weekday = datetime.datetime.today().weekday()
    day_delta = 0

    for day in day_array:
      if day < current_weekday:
        day_delta = current_weekday + 7

  
  #Email Construction
  body = "Ride Request:"
  msg_html = render_to_string('email.html', {
    'rider_first': current_user.first_name,
    'rider_last': current_user.last_name,
    'date': pickup_datetime,
    'time' : appointment_time,
    'pickup' : pickup_full_address,
    'dropoff' : dropoff_full_address,
    'ambulatory': amb_txt,
    'round_trip': trip_txt,
    'acc_name' : accompany_name,
    'pickup_number': pickup_phone,
    'dropoff_number': dropoff_phone,
    'acc_number' : accompany_number
    })
    
  full_name = current_user.first_name + " " + current_user.last_name
  send_mail(
    'RIDE REQUEST: {}'.format(full_name),
    body,
    'paulwinegard@gmail.com',
    ['paulwinegard@gmail.com'],
    fail_silently=False,
    html_message=msg_html,
  )

  return redirect("/manage_rides")

def delete_all(request):
  User.objects.all().delete() 
  return redirect("/")
def delete_all_rides(request):
  Ride.objects.all().delete() 
  PastRide.objects.all().delete() 

  
  return redirect("/")

def send_email(request):
  current_user = User.objects.get(id= request.session['current_user'])
  current_email = current_user.email
  current_name = current_user.first_name + " " + current_user.last_name
  subject = request.POST['email_subject']
  body = request.POST['email_body'] 
  print(body)

  msg_html = render_to_string('support_email.html', {
      'name' : current_name,
      'email' : current_email,
      'body' : body
  })

  send_mail(
    'SUPPORT: {}'.format(subject),
    body,
    'paulwinegard@gmail.com',
    ['paulwinegard@gmail.com'],
    fail_silently=False,
    html_message = msg_html
  )
  return redirect("/welcome")

def logout(request):
  del request.session['current_user']
  return redirect('/')

# Password rest
def password_reset(request):
  return render(request, 'registration/password_reset_form.html')
def password_reset_done(request):
  print('wassup mutha fucka')
  email = request.POST['email']
  msg_html = render_to_string('registration/password_reset_email.html')
  subject = "Papuga Password Reset"
  body = "Password Reset"
  print(body)

  send_mail(
    'SUPPORT: {}'.format(subject),
    body,
    'paulwinegard@gmail.com',
    [email],
    fail_silently=False,
    html_message = msg_html,
  )
  return render(request, 'registration/password_reset_done.html')
def password_reset_confirm(request):
  return render(request, 'registration/password_reset_confirm.html')
def password_reset_complete(request):
  return render(request, 'registration/password_reset_complete.html')