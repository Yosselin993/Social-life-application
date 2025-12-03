# clubs/views.py
from django.shortcuts import render, redirect
from .models import Club
from django.shortcuts import render, redirect, get_object_or_404

def browse_all_clubs(request):
    clubs = Club.objects.all()  # get all clubs from database
    # Show the browse_all.html page and give it the list of clubs
    return render(request, 'content/browse_all.html', {'clubs': clubs})

from django.contrib.auth.decorators import login_required
from .forms import EventForm 

@login_required
def add_event(request):
    if not request.user.clubs_led.exists():  # only club leaders can add events
        return redirect('mainPage')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # Assign the event to the first club the user leads (you can enhance this later)
            event.club = request.user.clubs_led.first()
            event.save()
            return redirect('events_calendar')
    else:
        form = EventForm()
    
    return render(request, 'content/add_event.html', {'form': form})


def club_profile(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, 'content/club_profile.html', {'club': club})
