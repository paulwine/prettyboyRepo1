# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
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
  rides = Ride.objects.all()
  context = {
    "rides" : rides
  }
  return render(request, "manage.html", context)
def info(request):
  current_user = User.objects.get(id= request.session['current_user'])
  context = {
    "user" : current_user
  }
  return render(request, "info.html", context)

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
  pickup_address = request.POST['pickup_address']
  pickup_city = request.POST['pickup_city']
  pickup_full_address = pickup_address + ", " + pickup_city
  pickup_room = request.POST['pickup_room']

  dropoff_address = request.POST['dropoff_address']
  dropoff_city = request.POST['dropoff_city']
  dropoff_full_address = dropoff_address + ", " + dropoff_city
  dropoff_room = request.POST['dropoff_room']
  dropoff_phone = request.POST['dropoff_phone']

  accompany_name = request.POST['accompany_name']
  accompany_number = request.POST['accompany_number']
  
  ambulatory = True
  round_trip = True
  if request.POST['ambulatory'] == True:
    ambulatory = True
  else:
    ambulatory = False
  
  if request.POST['round_trip'] == True:
    round_trip = True
  else:
    round_trip = False
    one_way = request.POST['one_way']

  duration = request.POST['duration']
  notes = request.POST['notes']

  if error == True:
    return redirect("/schedule_ride")
  else:
    ride = Ride.objects.create(pickup_address=pickup_full_address, pickup_datetime=pickup_datetime, pickup_room=pickup_room, dropoff_address= dropoff_full_address, facility_number=dropoff_phone, dropoff_room=dropoff_room, duration= duration, accompany_name= accompany_name, accompany_number=accompany_number, ambulatory= ambulatory, round_trip=round_trip, comments=notes, user=current_user)
    ride.save()

  return redirect("/manage_rides")

def delete_all(request):
  User.objects.all().delete() 
  return redirect("/")
# Create your views here.
