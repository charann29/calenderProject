from django.contrib import admin
from django.urls import path,include
from .views import GoogleCalendarInitView ,GoogleCalendarRedirectView


urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView, name='calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView, name='calendar-redirect'),
]