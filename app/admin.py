from django.contrib import admin
from .models import Movie, Actor, Director, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'director', 'is_top']
    list_filter = ['year', 'is_top', 'director']
    search_fields = ['title', 'description', 'director__name', 'actors__name']
    list_editable = ['is_top']
    filter_horizontal = ['actors']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'year', 'description', 'poster')
        }),
        ('Создатели', {
            'fields': ('director', 'actors')
        }),
        ('Дополнительно', {
            'fields': ('is_top',)
        }),
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'movie', 'rating', 'created_at', 'is_active']
    list_filter = ['rating', 'created_at', 'movie', 'is_active']
    search_fields = ['author_name', 'text', 'movie__title']
    readonly_fields = ['created_at']
    list_editable = ['is_active']