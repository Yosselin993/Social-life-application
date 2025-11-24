from django.db import models

class MyImageModel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/') # Images will be stored in media/images/

    def __str__(self):
        return self.title