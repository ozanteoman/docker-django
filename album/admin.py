from django.contrib import admin
from album.models import Song, Artist, Album

# Register your models here.

admin.site.register(Song)
admin.site.register(Artist)
admin.site.register(Album)
