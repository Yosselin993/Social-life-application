from django import forms
from .models import Club, Event #brings in the Club model so this form knows what data it works with

# this makes a form that is connected to the Club model
class ClubForm(forms.ModelForm):
    # the form should use these Club model
    class Meta:
        model = Club
        fields = ['name', 'description', 'meeting_time', 'location', 'leaders', 'descriptions', 'photo', 'banner']
        # these are the model fields we want to show on the form
        widgets = { #added
            'descriptions': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}), 
        }

class EventForm(forms.ModelForm): #make a form that is connected to the Event model
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )

    location = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    class Meta: 
        model = Event #this form will use the event model
        fields = ['title', 'description', 'date', 'time', 'location']  #fields from omdel we want to show in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }