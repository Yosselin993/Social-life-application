# clubs/views.py
from django.shortcuts import render
from .models import Club

def browse_all_clubs(request):
    clubs = Club.objects.all()  # get all clubs from database
    # Show the browse_all.html page and give it the list of clubs
    return render(request, 'content/browse_all.html', {'clubs': clubs})
