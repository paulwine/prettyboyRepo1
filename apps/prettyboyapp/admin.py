# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created_at']
    class Meta:
        model = User

class RideModelAdmin(admin.ModelAdmin):
    list_display = ['pickup_datetime', 'pickup_address', 'dropoff_address','created_at', 'approved']
    list_filter = ['approved', 'created_at', 'pickup_datetime']
    class Meta:
        model = Ride
# Register your models here.
admin.site.register(User, UserModelAdmin)
admin.site.register(Ride, RideModelAdmin)
