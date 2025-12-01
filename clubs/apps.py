from django.apps import AppConfig

# This sets up settings for the app called "clubs".
class ClubsConfig(AppConfig):
    #Tell Django to give each item a BIG ID number.
    default_auto_field = 'django.db.models.BigAutoField'
     # This is the app’s name. 
    name = 'clubs'
