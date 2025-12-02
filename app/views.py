from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Movie, Actor, Director, Review
from .forms import ReviewForm, MovieForm, DirectorForm, ActorForm, CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()


# Проверка является ли пользователь менеджером/администратором
def is_manager(user):
    return user.is_authenticated and user.is_staff


# Главная страница - доступна всем
def index(request):
    movies = Movie.objects.all().order_by('-year')

    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(actors__name__icontains=query) |
            Q(director__name__icontains=query)
        ).distinct()

    top_count = Movie.objects.filter(is_top=True).count()

    # Управление топом - только для менеджеров
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        action = request.POST.get('action')

        if movie_id and action and is_manager(request.user):
            movie = get_object_or_404(Movie, id=movie_id)

            if action == 'add_to_top':
                if top_count >= 5:
                    messages.error(request, 'В топе может быть не более 5 фильмов!')
                else:
                    movie.is_top = True
                    movie.save()
                    messages.success(request, f'"{movie.title}" добавлен в топ!')
            elif action == 'remove_from_top':
                movie.is_top = False
                movie.save()
                messages.success(request, f'"{movie.title}" удален из топа!')
            return redirect('index')

    context = {
        'movies': movies,
        'query': query,
        'top_count': top_count
    }
    return render(request, 'index.html', context)


# Детальная страница фильма - доступна всем
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.filter(is_active=True).order_by('-created_at')
    form = ReviewForm() if request.user.is_authenticated else None

    if request.method == 'POST':
        # Управление топом - только для менеджеров
        action = request.POST.get('action')

        if action in ['add_to_top', 'remove_from_top']:
            if is_manager(request.user):
                if action == 'add_to_top':
                    top_count = Movie.objects.filter(is_top=True).count()
                    if top_count >= 5:
                        messages.error(request, 'В топе может быть не более 5 фильмов!')
                    else:
                        movie.is_top = True
                        movie.save()
                        messages.success(request, f'"{movie.title}" добавлен в топ!')
                elif action == 'remove_from_top':
                    movie.is_top = False
                    movie.save()
                    messages.success(request, f'"{movie.title}" удален из топа!')
            else:
                messages.error(request, 'Только менеджеры могут управлять топом фильмов!')

            return redirect('movie_detail', movie_id=movie_id)

        # Добавление отзыва - только для зарегистрированных пользователей
        elif 'review_submit' in request.POST:
            if request.user.is_authenticated:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.movie = movie
                    review.author_name = request.user.username
                    review.save()
                    messages.success(request, '✅ Ваш отзыв успешно добавлен!')
                    return redirect('movie_detail', movie_id=movie_id)
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f'{field}: {error}')
            else:
                messages.error(request, 'Для добавления отзыва необходимо войти в систему!')
                return redirect('movie_detail', movie_id=movie_id)

    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'average_rating': movie.average_rating(),
        'reviews_count': reviews.count(),
    }
    return render(request, 'movie_detail.html', context)


# === ФУНКЦИИ ДОБАВЛЕНИЯ КОНТЕНТА (ТОЛЬКО ДЛЯ МЕНЕДЖЕРОВ) ===

@user_passes_test(is_manager, login_url='/accounts/login/')
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Фильм "{movie.title}" успешно добавлен!')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()

    return render(request, 'add_content.html', {
        'form': form,
        'title': 'Добавить фильм',
        'type': 'movie'
    })


@user_passes_test(is_manager, login_url='/accounts/login/')
def add_director(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            director = form.save()
            messages.success(request, f'Режиссер "{director.name}" успешно добавлен!')
            return redirect('directors_list')
    else:
        form = DirectorForm()

    return render(request, 'add_content.html', {
        'form': form,
        'title': 'Добавить режиссера',
        'type': 'director'
    })


@user_passes_test(is_manager, login_url='/accounts/login/')
def add_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            actor = form.save()
            messages.success(request, f'Актер "{actor.name}" успешно добавлен!')
            return redirect('actors_list')
    else:
        form = ActorForm()

    return render(request, 'add_content.html', {
        'form': form,
        'title': 'Добавить актера',
        'type': 'actor'
    })


# === РЕГИСТРАЦИЯ И АВТОРИЗАЦИЯ ===

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            # Отправляем email СРАЗУ ЖЕ в этом же процессе
            print("\n" + "=" * 50)
            print("РЕГИСТРАЦИЯ: Пытаюсь отправить welcome email")
            print(f"Пользователь: {user.username}")
            print(f"Email: {user.email}")
            print("=" * 50 + "\n")

            try:
                subject = f'Добро пожаловать в {settings.SITE_NAME}!'

                # Контекст для шаблона
                context = {
                    'user': user,
                    'site_name': settings.SITE_NAME,
                    'site_domain': settings.SITE_DOMAIN,
                    'ADMIN_EMAIL': settings.ADMIN_EMAIL,
                }

                # Рендерим HTML и текстовую версию
                html_message = render_to_string('emails/welcome_email.html', context)
                plain_message = strip_tags(html_message)

                # Показываем в консоли что отправляем
                print(f"Отправляю письмо с темой: {subject}")
                print(f"От: {settings.DEFAULT_FROM_EMAIL}")
                print(f"Кому: {user.email}")
                print(f"Бэкенд email: {settings.EMAIL_BACKEND}")

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )

                print("✅ Письмо отправлено успешно!")

            except Exception as e:
                print(f"❌ Ошибка при отправке письма: {e}")
                import traceback
                traceback.print_exc()

            # Автоматический вход после регистрации
            login(request, user)

            messages.success(request,
                             f'Регистрация успешна! Добро пожаловать, {user.username}! '
                             f'На ваш email ({user.email}) отправлено приветственное письмо.'
                             )
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')


# === ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ===

@login_required
def profile_view(request):
    user = request.user
    user_movies = Movie.objects.all().count()  # Просто общее количество для демонстрации
    user_reviews = Review.objects.filter(author_name=user.username).count()

    context = {
        'user': user,
        'user_movies': user_movies,
        'user_reviews': user_reviews,
    }
    return render(request, 'profile.html', context)


# === ОСТАЛЬНЫЕ ФУНКЦИИ ===

def top_five(request):
    top_movies = Movie.objects.filter(is_top=True).order_by('-year')
    context = {
        'top_movies': top_movies
    }
    return render(request, 'top_five.html', context)


def directors_list(request):
    directors = Director.objects.all().order_by('name')
    context = {
        'directors': directors
    }
    return render(request, 'directors_list.html', context)


def actors_list(request):
    actors = Actor.objects.all().order_by('name')
    context = {
        'actors': actors
    }
    return render(request, 'actors_list.html', context)


def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    movies = Movie.objects.filter(actors=actor).order_by('-year')
    context = {
        'actor': actor,
        'movies': movies
    }
    return render(request, 'actor_detail.html', context)


def director_detail(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    movies = Movie.objects.filter(director=director).order_by('-year')
    context = {
        'director': director,
        'movies': movies
    }
    return render(request, 'director_detail.html', context)