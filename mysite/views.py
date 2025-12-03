from itertools import product
from django.shortcuts import render #import render function, it helps to render HTML templates
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm #added
from clubs.models import Club
from clubs.models import Event
from clubs.forms import ClubForm


from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student
# this is a function that handles requests to the home page
def home(request): 
    return render(request, 'home.html') #render function to generate and return an HTML response
def search_view(request):
    search_term = request.GET.get('search_query', '') # Get the search query 
    if search_term:
        # Filter your model objects based on the search term
        # Example: searching in 'title' and 'description' fields of a 'Product' model
        results = product.objects.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        ).order_by('name') # Order your results as needed
    else:
        results = product.objects.all().order_by('name') # Show all if no search term

    context = {
        'results': results,
        'search_term': search_term,
    }
    return render(request, 'home.html', context)

def index_view(request):
    return render(request, 'myapp/index.html')

def home_view(request):
    return render(request, 'myapp/home.html')

def about_view(request):
    return render(request, 'myapp/about.html')

def user_login(request):
    # if user is already logged in, send them to the main page
    # if request.user.is_authenticated:
    #   return redirect('mainPage')  # Replace 'main_page' with your desired redirect URL name

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) #authenticate the user

        if user is not None:
            login(request, user)

            #added
            if user.clubs_led.exists():
                club = user.clubs_led.first()
                if not club.first_login_completed:
                    return redirect('club_first_login')
    
            messages.success(request, "Login successful!") #added this messae
            return redirect('mainPage')  # Redirect to a home page after successful login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')


@login_required(login_url='login')
def main_page(request):
    club = None
    club_form = None
    is_club_leader = request.user.clubs_led.exists()

    if is_club_leader:
        club = request.user.clubs_led.first()
        if not club.first_login_completed:
            from clubs.forms import ClubForm
            club_form = ClubForm(instance=club)

    # Get or create a Student instance for the current user
    student, created = Student.objects.get_or_create(user=request.user)

    # Handle photo upload
    if request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('mainPage')
        else:
            messages.error(request, "Error uploading photo. Please try again.")
    else:
        student_form = StudentForm(instance=student)

    context = {
        'form': student_form,
        'student': student,
        'is_club_leader': is_club_leader,
        'club_form': club_form,
        'club': club,
    }

    return render(request, 'content/mainPage.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')   # Redirect to the login page after logout

#added
def signup_role(request): #handles the first signup page where the user chooses their role
    return render(request, 'registration/signup_role.html') #renders the HTML page that asks "who are you"

def signup_user(request, role): #handles the actual signup form based on the role selected
    if role not in ['student', 'club']: #if the role is not student or club, redirect back to selection page
        return redirect('signup_role')  # invalid role chosen

    if request.method == 'POST': #if the form was submitted (method is POST), process the form data
        form = UserCreationForm(request.POST)
        if form.is_valid(): #check if the submitted form is valid (all fields filled and passwords match)
            new_user = form.save() #save the new user to the database

            if role == 'club':
                # Create the Club object. It will have default/blank fields.
                new_club = Club.objects.create(
                    name=f"New Club - {new_user.username}'s Club",
                )
                # Link the user as a leader (this populates clubs_led)
                new_club.leaders.add(new_user)
            
            messages.success(request, "Account created successfully! You can now log in.") #show a success message telling the user their account was created
            
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
            form = UserCreationForm()

    return render(request, 'registration/signup_user.html', {'form': form, 'role': role}) #rend the signup page with the form and the chosen role

@login_required
def upload_image_view(request):
    # Get or create a Student instance for the current user
    student, created = Student.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('upload_photo')
        else:
            messages.error(request, "Error uploading photo. Please try again.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'content/mainPage.html', {'form': form, 'student': student})

#python's calendar and datetime dynamic based for calendar
import calendar 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta #if this doesn't work, install this in your virtual environment "pip install python-dateutil"
from django.shortcuts import render

@login_required
def events_calendar(request, year=None, month=None):
    #current month and year
    today = date.today()

    if year is None or month is None:
        display_date = today #if no month/year provided, use current month
    else:
        try:
            display_date = date(int(year), int(month), 1) #if month/year provided, use those values
        except ValueError:
            display_date = today #handle invalid month/year

    year = display_date.year
    month = display_date.month

    #calculate the first day of the *next* month
    next_date = display_date + relativedelta(months=1)

    #check to see if the currently displayed month is the current month
    is_current_month = (year == today.year and month == today.month)

    #navigation links 
    next_month_year = next_date.year
    next_month_num = next_date.month

    #calculate the month name for the title
    current_month_name = datetime(year, month, 1).strftime('%B')

    #get the number of days in month
    num_days = calendar.monthrange(year,month)[1] #returns weekday of 1st, number of days

    #get the weekday os the 1st day of month (0=monday, 6=sunday)
    first_weekday = calendar.monthrange(year,month)[0]
    first_weekday = (first_weekday + 1) % 7

    #create a list of day numbers
    days = list(range(1, num_days + 1))
    blank_days = list(range(first_weekday)) #list for empty boxes

    # events loaded from database
    events = Event.objects.filter(month=month, year=year)

    return render(request, "content/events_calendar.html", {
        "year": year,
        "month": month,
        "month_name": current_month_name, 
        "days": days,
        "blank_days": blank_days,
        "events":events,
         #passing this template to know where to start

         "next_month_year": next_month_year,
         "next_month_num": next_month_num,
         "is_current_month": is_current_month,
         "user": request.user, #added
         "is_club_leader": request.user.clubs_led.exists() #added
    })

#def browse_all(request):
    #return render(request, 'content/Browse_All.html')
def browse_all(request):
    clubs = Club.objects.all()  # get all clubs from the database
    return render(request, 'content/Browse_All.html', {'clubs': clubs})


@login_required
def club_first_login(request):
    #ensure the user is a club leader and retrieve their club
    if not request.user.clubs_led.exists():
        return redirect('mainPage') #user is not a leader or club wasn't created
    
    club = request.user.clubs_led.first()
    
    if club.first_login_completed: #check if the setup is already complete
        return redirect('mainPage')
    
    if request.method == 'POST':
        form = ClubForm(request.POST, instance = club)
        if form.is_valid():
            club = form.save(commit=False)
            club.first_login_completed = True
            club.save()
            form.save_m2m() #important for many to many fields
            messages.success(request, f"Welcome to the platform, {club.name}!")
            return redirect('mainPage')
    else:
        form = ClubForm(instance=club) #load the form with the exisiting club data

    return render(request, 'content/club_first_login.html', {'form': form})


