# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User, Ride
import bcrypt
  # the index function is called when root is visited
def index(request):
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
  phone = request.POST['phone']
  address = request.POST['address']
  info = request.POST['info']
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
  if len(phone) < 1:
    messages.error(request, 'Please input a valid phone number')
    error = True
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
    new_user = User.objects.create(first_name=first, last_name=last, email=email, password=password, special=info, primary_address=address, phone=phone)
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
  context = {
    "user" : current_user
  }
  return render(request, "schedule.html", context)
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
  dropoff_phone = request.POST['dropoff_phone']

  accompany_name = request.POST['accompany_name']
  accompany_number = request.POST['accompany_number']
  
  ambulatory = True
  round_trip = True

  amb_txt = "Ambulatory"
  trip_txt = "Round Trip"

  if request.POST['ambulatory'] == True:
    ambulatory = True
  else:
    ambulatory = False
    amb_txt = "Wheelchair Bound"
  
  if request.POST['round_trip'] == True:
    round_trip = True
  else:
    round_trip = False
    trip_txt = "One Way"
    one_way = request.POST['one_way']

  duration = request.POST['duration']
  notes = request.POST['notes']

  if error == True:
    return redirect("/schedule_ride")
  else:
    ride = Ride.objects.create(pickup_address=pickup_full_address, pickup_datetime=pickup_datetime, appointment_time= appointment_time,pickup_room=pickup_room, dropoff_address= dropoff_full_address, facility_number=dropoff_phone, dropoff_room=dropoff_room, duration= duration, accompany_name= accompany_name, accompany_number=accompany_number, ambulatory= ambulatory, round_trip=round_trip, comments=notes, user=current_user)
    ride.save()

  
  #Email Construction
  body = "BODY BABY"
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

def send_email(request):
  current_user = User.objects.get(id= request.session['current_user'])
  current_email = current_user.email
  subject = request.POST['email_subject']
  body = request.POST['email_body']
  print(body)

  send_mail(
    'SUPPORT: {}'.format(subject),
    body,
    'paulwinegard@gmail.com',
    ['paulwinegard@gmail.com'],
    fail_silently=False,
  )
  return redirect("/welcome")
# Create your views here.
