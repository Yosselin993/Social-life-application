from django_summernote.widgets import SummernoteWidget #3rd party package (not built into django) that turns a simple text area into an editor
from .models import Comment
from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm #added
from django.contrib.auth.models import User #added
from mysite.custom_clean import SafeSummernoteField
from.models import Announcement
from .models import Post 
# NEW import for post comments
from .models import PostComment

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


#for the quiz
#a python list of tuples for quiz interests
#first element of each tuple is the actual value stored in database
#second element is the human-readbale label showm in the form
#django uses this list to populate checkboxes in forms automatically
INTEREST_CHOICES = [
    ("technology", "Technology"),
    ("sports", "Sports"),
    ("community", "Community Service"),
    ("arts", "Arts & Creativity"),
    ("leadership", "Leadership"),
    ("culture", "Cultural Clubs"),
    ("gaming", "Gaming & Esports"),
]

MAJOR_CHOICES = [ #used for a dropdown (choicefield) instead of checkboxes
    ('', 'Select your major'),  #blank option, ensures suer can leave it empty
    ('computerscience', 'Computer Science'),
    ('politicalscience', 'Political Science'),
    ('biology', 'Biology'),
    ('environmental', 'Environmental Science'),
    ('premed', 'Pre-Med'),
    ('health', 'Health Sciences'),
    ('psychology', 'Psychology'),
    ('socialscience', 'Social Sciences'),
    ('marketing', 'Marketing'),
    ('media', 'Media Studies'),
    ('communications', 'Communications'),
    ('business', 'Business'),
    ('engineering', 'Engineering'),
    ('mathematics', 'Mathematics'),
    ('economics', 'Economics'),
    ('other', 'Other'),
]


class QuizForm(forms.Form): #django validates the selected values against interest_choices and provides cleaned_data
    interests = forms.MultipleChoiceField( #lets users select more than one interest
        choices = INTEREST_CHOICES,
        widget = forms.CheckboxSelectMultiple, #tells django to render checkboxes instead of a multi-select dropdown
        required=True, #ensures at least one checkbox must be checked
        label="Select your interests"
    )

    major = forms.ChoiceField( #renders a dropdown menu with major_choices
        choices = MAJOR_CHOICES, 
        required = False, #allows user to skip this field
        label = "Select your major"
    ) #django validates that the submitted value matches on of the allowed choices


class AnnouncementForm(forms.ModelForm):
    content = SafeSummernoteField()   # override the field to avoid bleach crash

    class Meta:
        model = Announcement
        fields = ['content']

class PostForm(forms.ModelForm):
    # Use a plain textarea for caption to avoid image uploads in the editor
    content = forms.CharField(label="Caption", widget=forms.Textarea(attrs={
        'rows': 4,                     # set textarea height to 4 rows
        'placeholder': 'Write a caption...'  # hint text shown inside the field
    }))
    image = forms.ImageField(required=False, label="Image")  # optional image upload field

    class Meta:
        model = Post                  # bind this form to the Post model
        fields = ['content', 'image'] # include only caption and image fields


class PostCommentForm(forms.ModelForm):
    text = forms.CharField(label="Comment", widget=forms.Textarea(attrs={
        'rows': 2,                     # smaller textarea for short comments
        'placeholder': 'Write a comment...'  # hint text for comment input
    }))
    class Meta:
        model = PostComment           # bind this form to the PostComment model
        fields = ['text']             # only a single text field for comments