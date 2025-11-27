"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views # the "." means current directory, so we are importing views.py from the current directory
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # When someone visits the home page ('/'), call the home view and name this URL 'home'
    path('search/', views.search_view, name='search'),
    path('index/', views.index_view, name='index'),
    path('home/', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_role, name = 'signup_role'), #added the url for the first signup page where the user chooses their role
    path('signup/<str:role>/', views.signup_user, name='signup_user'), #added url for the actual signup form (dynamically changes depending on the selected role)
    path("content/mainPage", views.main_page, name="mainPage"), #changed
    path('upload-photo/', views.upload_image_view, name='upload_photo'),
    path("events/", views.events_calendar, name = "events_calendar"), #url for the events calendar
    path('calendar/<int:year>/<int:month>/', views.events_calendar, name = 'events_calendar_nav'), #path for navigaing to a specific month/year
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)