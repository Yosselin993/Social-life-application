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
            messages.success(request, "Login successful!") #added this messae
            return redirect('mainPage')  # Redirect to a home page after successful login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')


def main_page(request):
    return render(request, 'content/mainPage.html')


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
            form.save() #save the new user to the database
            messages.success(request, "Account created successfully! You can now log in.") #show a success message telling the user their account was created
            form = UserCreationForm() #resets the form so page doesn't show filled data
        else:
            messages.error(request, "Please correct the errors below.")
    else:
            form = UserCreationForm()

    return render(request, 'registration/signup_user.html', {'form': form, 'role': role}) #rend the signup page with the form and the chosen role

#python's calendar and datetime dynamic based for calendar
import calendar 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta #if this doesn't work, install this in your virtual environment "pip install python-dateutil"
from django.shortcuts import render

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

    #dummy events
    events = [
        {"title": "Chess Club @ 5pm", "day": 3, "month": 12, "year": year},
        {"title": "AI Workshop @ 6:30pm", "day": 10, "month": 12, "year": year},
        {"title": "Robotics Club @ 3:15pm", "day": 15, "month": 12, "year": year},
    ]

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
    })

