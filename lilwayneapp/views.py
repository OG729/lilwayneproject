"""
Django views for handling user authentication, homepage, albums, songs, and user profiles.

This module contains functions for rendering different views related to the music website.
These views include user authentication, displaying the homepage, albums, and songs, and managing user profiles.

Functions:
    - `signup(request)`: Handles user registration and redirects to the user's profile upon successful registration.
    - `homepage(request)`: Renders the homepage with the artist's profile information.
    - `albums(request)`: Fetches and displays a list of albums without including artist_id.
    - `songs(request)`: Fetches and displays a list of songs.
    - `profile(request)`: Renders the user's profile page, allowing users to vote for their favorite song in a poll.

Dependencies:
    - Django: Python web framework for building web applications.
    - `render` and `redirect` functions from `django.shortcuts` for rendering templates and redirecting requests.
    - `login_required` decorator from `django.contrib.auth.decorators` for restricting access to authenticated users.
    - `CustomUserCreationForm`, `PollForm`, `Song`, `Album`, `ArtistProfile`, and `Poll` models from the application.
    - `login` function from `django.contrib.auth` for user authentication and login.

Note:
    Ensure the appropriate Django models and forms are imported for the views to work correctly.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Song, Album, ArtistProfile
from .forms import CustomUserCreationForm, PollForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PollForm  # Import your PollForm here
from .models import Poll

def signup(request):
    """
    Handles user registration and redirects to the user's profile upon successful registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the user's profile page after successful registration or renders the registration form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to the user's profile after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def homepage(request):
    """
    Renders the homepage with the artist's profile information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the homepage template with the artist's profile information.
    """
    artist_profile = ArtistProfile.objects.first()
    context = {
        'artist_profile': artist_profile,
    }
    return render(request, 'homepage.html', context)

def albums(request):
    """
    Fetches and displays a list of albums without including artist_id.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the albums template with the list of albums.
    """
    # Fetch a list of albums without including artist_id
    albums_list = Album.objects.all().values('title', 'release_date')

    context = {
        'albums_list': albums_list,
    }
    return render(request, 'albums.html', context)

def songs(request):
    """
    Fetches and displays a list of songs.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the songs template with the list of songs.
    """
    songs_list = Song.objects.all()
    context = {
        'songs_list': songs_list,
    }
    return render(request, 'songs.html', context)

@login_required
def profile(request):
    """
    Renders the user's profile page, allowing users to vote for their favorite song in a poll.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the user's profile template with the poll form and favorite songs list.
    """
    favorite_songs = ['A Milli', 'Lollipop', '6 Foot 7 Foot', 'How to Love', 'No Worries']
    success_message = None

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            # Get the selected song from the form
            selected_song = form.cleaned_data['favorite_song']
            
            # Get the user making the poll
            user = request.user
            
            # Check if the user has already voted
            existing_vote = Poll.objects.filter(user=user).first()
            
            if existing_vote:
                # User has already voted, update the existing vote
                existing_vote.favorite_song = selected_song
                existing_vote.save()
            else:
                # User has not voted yet, create a new poll entry
                Poll.objects.create(user=user, favorite_song=selected_song)
            
            success_message = 'Poll submitted successfully!'
        else:
            # Form is not valid, handle the errors if needed
            pass
    else:
        form = PollForm()

    return render(request, 'registration/profile.html', {'form': form, 'favorite_songs': favorite_songs, 'success_message': success_message})
