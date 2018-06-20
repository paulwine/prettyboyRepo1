from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registerpage$', views.registerpage),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^contact$', views.contact),
    url(r'^schedule_ride$', views.schedule_ride),
    url(r'^manage_rides$', views.manage_rides),
    url(r'^info$', views.info),
    url(r'^all_users$', views.all_users),
    url(r'^submit_ride$', views.submit_ride),
    
    # temp
    url(r'^delete_all$', views.delete_all)

]
