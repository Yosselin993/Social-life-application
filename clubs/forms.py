from django import forms
from .models import Club # brings in the Club model so this form knows what data it works with

# this makes a form that is connected to the Club model
class ClubForm(forms.ModelForm):
    # the form should use these Club model
    class Meta:
        model = Club
        fields = ['name', 'description', 'meeting_time', 'location', 'leaders', 'descriptions']
        # these are the model fields we want to show on the form
