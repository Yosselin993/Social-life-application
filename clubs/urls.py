from django.urls import path
from . import views
# This list holds all the URL patterns for this app clubs
urlpatterns = [
    # When someone goes to "/all/", run the browse_all_clubs view
    # and name this URL "browse_all_clubs" so we can use it in templates
    path('all/', views.browse_all_clubs, name='browse_all_clubs'),
    path('add-event/', views.add_event, name='add_event'), #goes to the add_event html to add the new event
    #adding individul club profile pages
    path('club/<int:club_id>/', views.club_profile, name='club_profile'), 
    #added the following to paths for an editing/deleting event for clubs
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]
