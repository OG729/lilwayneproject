from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class ArtistProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='artist_profiles/')
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)

class Album(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)

class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)

class CustomUser(AbstractUser):
    # Add custom fields here (without 'profile_picture')
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add other fields for user profiles as needed

    def __str__(self):
        return self.user.username  # Return a meaningful representation of the user profile

class Poll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorite_song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_polls')
    favorite_album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_polls')
