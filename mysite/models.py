from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from clubs.models import Club #added for annoucements

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Student Profile"
        return f"Student {self.id}"

class Comment(models.Model):
    # A text field that uses the Summernote editor for formatting
    text = SummernoteTextField()

#store annoucements, annoucement model linked to club
class Announcement (models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # latest first