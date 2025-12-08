from django_summernote.widgets import SummernoteWidget
from .models import Comment
from django import forms
from .models import Student

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