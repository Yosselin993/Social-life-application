from django.contrib import admin
from .models import Club, Event


# Register your models here.

#this is where we tell Django how our models should look in the admin

class ClubAdmin(admin.ModelAdmin): #makes a custom admin view for the club model
    list_display = ('name', 'meeting_time', 'location', 'first_login_completed')  #show columns in admin list for clubs
    search_fields = ('name', 'description', 'descriptions') #allow admin users to search clubs by these fields
    filter_horizontal = ('leaders',) #shows a horizontal widget for selecting multiple leaders

class EventAdmin(admin.ModelAdmin): #make a custom admin view for the event model
    list_display = ("title", "club", "date", "time", "location")
    list_filter = ("club", "date")   # removed month/year/day — they no longer exist
    search_fields = ("title", "description", "location")

# Only register if not already registered
if not admin.site.is_registered(Club):
    admin.site.register(Club, ClubAdmin)

if not admin.site.is_registered(Event):
    admin.site.register(Event, EventAdmin)
