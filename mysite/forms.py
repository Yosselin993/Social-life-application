from django_summernote.widgets import SummernoteWidget
from .models import Comment
from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm #added
from django.contrib.auth.models import User #added

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['photo']

class CommentForm(forms.ModelForm):
    class Meta:
        # Tell Django this form is based on the Comment model
        model = Comment
        # These are the fields from the model that will appear in the form
        fields = ('text',)
        # Use the Summernote editor widget for the text area
        widgets = {
            'text': SummernoteWidget(),
        }

class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)

        #show first/last name ONLY for students
        if role != 'student':
            self.fields.pop('first_name')
            self.fields.pop('last_name')

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name")