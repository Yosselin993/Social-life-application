from django import forms
from .models import Club, Event #brings in the Club model so this form knows what data it works with
from datetime import datetime #import datetime to set a default initial time value for the time picker

# this makes a form that is connected to the Club model
class ClubForm(forms.ModelForm):
    # the form should use these Club model
    meeting_time = forms.TimeField(  #customizing the meeting_time field
    required=True, #django validation: user must select a time
    initial=datetime.now().strftime("%H:%M"), #native HTML5 time pickers (browser provides UI)
    widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}) #bootstrap styling for consistent look
)

#django provides form validation and rendering
#bootstrap provides the styling of the input field

    class Meta:
        model = Club #link this form to the club model
        fields = ['name', 'description', 'meeting_time', 'location', 'leaders', 'descriptions', 'photo', 'banner'] #specify which fields from the models should appear on the form
        # these are the model fields we want to show on the form
        widgets = { #allow customizing the HTML rendering of specific fields
            'descriptions': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}), 
        }

class EventForm(forms.ModelForm): #form for creating or editing an event
    date = forms.DateField( #date input field
        widget=forms.DateInput(attrs={
            'type': 'date', #native HTML5 daye picker (broweser handles calendar popup)
            'class': 'form-control' #bootstrap styling
        })
    )

    time = forms.TimeField( #time input field
        widget=forms.TimeInput(attrs={
            'type': 'time', #native HTML5 time picker (browser clock popup)
            'class': 'form-control' #bootstrap styling
        })
    )

    location = forms.CharField( #location field = text input
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    class Meta: 
        model = Event #this form will use the event model
        fields = ['title', 'description', 'date', 'time', 'location']  #fields from omdel we want to show in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), #customize title field with bootstrap styling
            'description': forms.Textarea(attrs={'class': 'form-control'}), #customzie description textarea with bootstrap
        }