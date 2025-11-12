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
    # Redirect authenticated users to a home page
    if request.user.is_authenticated:
        return redirect('content/mainPage')  # Replace 'main_page' with your desired redirect URL name

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page after successful login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')


def main_page(request):
    return render(request, 'content/mainPage.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')   # Redirect to the home page after logout

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
            messages.success(request, f"{role.capitalize()} account created successfully!") #show a success message telling the user their account was created
            return redirect('login') #after signup, send the user to the login page
    else:
        form = UserCreationForm() #if the page is just opened, (not submitted yet), show a blank signup form

    return render(request, 'registration/signup_user.html', {'form': form, 'role': role}) #rend the signup page with the form and the chosen role
