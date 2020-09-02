from django.conf.urls import url
from django.contrib.auth import views as auth_views

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
    url(r'^select_past_ride$', views.select_past_ride),
    url(r'^schedule_ride_from_past_ride/(?P<rideid>\d+)/$', views.schedule_ride_from_past_ride),
    url(r'^schedule_ride_from_denied_ride/(?P<rideid>\d+)/$', views.schedule_ride_from_denied_ride),
    url(r'^submit_past_ride$', views.submit_past_ride),
    url(r'^submit_denied_ride$', views.submit_denied_ride),
    url(r'^info$', views.info),
    url(r'^all_users$', views.all_users),
    url(r'^submit_ride$', views.submit_ride),
    url(r'^send_email$', views.send_email),
    url(r'^save_information$', views.save_information),
    url(r'^delete_ride/(?P<rideid>\d+)/$', views.delete_ride),
    url(r'^logout$', views.logout),
    # temp
    url(r'^delete_all$', views.delete_all),
    url(r'^delete_all_rides$', views.delete_all_rides),
    #password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

]
