from itertools import product
from django.shortcuts import render #import render function, it helps to render HTML templates
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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
    return redirect('home')  # Redirect to the home page after logout
