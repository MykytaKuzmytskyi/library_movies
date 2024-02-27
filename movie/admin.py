from django.contrib import admin

from movie.models import Actor, Movie, Director

admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Movie)
