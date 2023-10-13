from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('albums/', views.albums, name='albums'),
    path('songs/', views.songs, name='songs'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),


    # User Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),  # Create a signup view in your views.py
    path('profile/', views.profile, name='profile'),  # Create a profile view in your views.py
]
