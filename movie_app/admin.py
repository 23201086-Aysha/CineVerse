from django.contrib import admin

# Register your models here.
from .models import Movie, Genre, Mood


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MoodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'mood', 'release_date')
    list_filter = ('genre', 'mood', 'release_date')
    search_fields = ('title', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'release_date')
        }),
        ('Categorization', {
            'fields': ('genre', 'mood')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Mood, MoodAdmin)
