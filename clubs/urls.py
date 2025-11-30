from django.urls import path
from . import views
# This list holds all the URL patterns for this app clubs
urlpatterns = [
    # When someone goes to "/all/", run the browse_all_clubs view
    # and name this URL "browse_all_clubs" so we can use it in templates
    path('all/', views.browse_all_clubs, name='browse_all_clubs'),
]
