from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    #The name of the club with max 100 char
    name = models.CharField(max_length=100)
    # They can give a longer description of what the club is about
    description = models.TextField(blank=True)
    # Giving the user the options to display when the club meets
    meeting_time = models.CharField(max_length=100, blank=True)
    #Where the clubs meet
    location = models.CharField(max_length=100, blank=True)
    
    # Multiple users can be leaders,or be leaders of more then one clubs
    leaders = models.ManyToManyField(User, blank=True, related_name="clubs_led")
    
    # Short labels for the club to write. They are one-word tags separated by commas
    descriptions = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Enter one-word descriptions separated by commas"
    )

    first_login_completed = models.BooleanField(default = False) #tracks if the first login/setup for this club has been done by true or false

    # How the club will be shown in Django admin or in print
    def __str__(self):
        return self.name
    
class Event(models.Model): #defined an event model (like a template for an event)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='events') #link this event to a club; if club deleted then event is deleted too
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    
    def __str__(self): #how the event shows up when events calendar
        return f"{self.title} ({self.club.name})"
    


