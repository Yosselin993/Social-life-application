from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from clubs.models import Club #added for annoucements
from clubs.models import Event

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) #links each profile to exactly one user (ensures deleting a user deletes their profile)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True) #stores an optional profile image

    def __str__(self):
        return f"{self.user.username}'s Profile" #returns a readable string for admin or console


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #one to one relationship with optional user
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True) #optional photo field

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Student Profile" #shows username if linked
        return f"Student {self.id}" #fallback if no user linked

class Comment(models.Model):
    # A text field that uses the Summernote editor for formatting
    text = SummernoteTextField()

#store annoucements, annoucement model linked to club
class Announcement (models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements') #access all announcements of a club via club.announcements 
    author = models.ForeignKey(User, on_delete=models.CASCADE) #stores the user who wrote the announcement
    content = models.TextField() #plain text content of the announcement 
    created_at = models.DateTimeField(auto_now_add=True) #timestamp automaticaly set when announcement is created

    class Meta:
        ordering = ['-created_at']  #default odering in queries , latest first


class Post(models.Model):
    club = models.ForeignKey(
        Club, 
        on_delete=models.CASCADE, 
        related_name='posts',
        null=True,    
        blank=True,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post in {self.club.name} by {self.author.username}"
    