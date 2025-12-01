from django import forms
from .models import Club, Event #brings in the Club model so this form knows what data it works with

# this makes a form that is connected to the Club model
class ClubForm(forms.ModelForm):
    # the form should use these Club model
    class Meta:
        model = Club
        fields = ['name', 'description', 'meeting_time', 'location', 'leaders', 'descriptions']
        # these are the model fields we want to show on the form
        widgets = { #added
            'descriptions': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}), 
        }

class EventForm(forms.ModelForm): #make a form that is connected to the Event model
    class Meta: 
        model = Event #this form will use the event model
        fields = ['title', 'description', 'day', 'month', 'year']  #fields from omdel we want to show in the form