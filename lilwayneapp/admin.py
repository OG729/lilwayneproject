from django.contrib import admin
from .models import ArtistProfile, Album, Song, UserProfile

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')  # Display fields in the admin list view

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'get_artist_name')
    search_fields = ('title', 'artist__name')

    def get_artist_name(self, obj):
        return obj.artist.name

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Display only 'title'
    search_fields = ('title',)  # Allow searching by 'title' only

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display 'user' field in the admin list view
