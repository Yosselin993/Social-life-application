# clubs/views.py
from django.shortcuts import render, redirect
from .models import Club, Event
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages #used to display one-time notfications to users
import datetime

def browse_all_clubs(request):
    clubs = Club.objects.all()  # get all clubs from database
    # Show the browse_all.html page and give it the list of clubs
    return render(request, 'content/browse_all.html', {'clubs': clubs})

from django.contrib.auth.decorators import login_required
from .forms import EventForm 

@login_required
def toggle_favorite(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.method == 'POST':
        if request.user in club.favorites.all():
            club.favorites.remove(request.user)
            messages.success(request, f"Removed {club.name} from favorites.")
        else:
            club.favorites.add(request.user)
            messages.success(request, f"Added {club.name} to favorites.")

    # Redirect back to where the request came from, or to the club profile
    return redirect(request.META.get('HTTP_REFERER') or 'club_profile')

@login_required
def add_event(request):
    # Only club leaders can add events
    if not request.user.clubs_led.exists():
        messages.error(request, "You must be a club leader to create events.")
        return redirect('mainPage')

    if request.method == 'POST':
        form = EventForm(request.POST)  # use the form to handle date & time
        if form.is_valid():
            event = form.save(commit=False)
            event.club = request.user.clubs_led.first()  # assign the club
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('events_calendar_nav', year=event.date.year, month=event.date.month)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = EventForm()

    return render(request, 'content/add_event.html', {'form': form})




def club_profile(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, 'content/club_profile.html', {'club': club})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id) #retrieves the event by id or return 404 if not found

    if request.user not in event.club.leaders.all(): #ensures current user is a leader of the event's club
        messages.error(request, "You cannot edit this event.") #shows error message
        return redirect('events_calendar')
    
    if request.method == 'POST': #if the form is submitted
        form = EventForm(request.POST, instance = event) #onnect submitted data to the form, using the existing event instance
        if form.is_valid():
            form.save() #save changes to the event
            messages.success(request, "Event updated successfully.")
            return redirect('events_calendar') #go back to calendar
    else:
        form = EventForm(instance=event) #if the request is GET, display the form pre-filled with event data

    return render(request, 'content/add_event.html', {'form': form, 'edit': True}) #render the same template as add_event but with an edit flag
    
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user not in event.club.leaders.all():
        messages.error(request, "You cannot delete this event.")
        return redirect('events_calendar')
    
    if request.method == 'POST':
        event.delete() #if confirmed, delete the event
        messages.success(request, "Event deleted successfully.")
        return redirect('events_calendar')

    return render(request, 'content/confirm_delete.html', {'event':event})