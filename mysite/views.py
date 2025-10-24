from django.shortcuts import render #import render function, it helps to render HTML templates

# this is a function that handles requests to the home page
def home(request): 
    return render(request, 'home.html') #render function to generate and return an HTML response
