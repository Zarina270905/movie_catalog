from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('top-five/', views.top_five, name='top_five'),
    path('directors/', views.directors_list, name='directors_list'),
    path('actors/', views.actors_list, name='actors_list'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('director/<int:director_id>/', views.director_detail, name='director_detail'),

    # Регистрация и авторизация
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),

    # Добавление контента (только для менеджеров)
    path('add/movie/', views.add_movie, name='add_movie'),
    path('add/director/', views.add_director, name='add_director'),
    path('add/actor/', views.add_actor, name='add_actor'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)