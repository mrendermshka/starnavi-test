from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Like, get_posts, post_creator, put_like
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


def auth_checker(request):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect("/feed/")

    return wrapper(request)


def main_view(request):
    auth_checker(request)
    return render(request, "main.html")


def register_page(request):
    auth_checker(request)
    return render(request, "signup.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/feed/')
    return render(request, "login.html")


@require_POST
def login_process(request):
    # Assuming the form data contains 'username' and 'password'
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    # Check if authentication was successful
    if user is not None:
        # Log in the user
        login(request, user)
        return redirect("/feed/")
    else:
        return HttpResponse("Invalid credentials. Please try again.")


@require_POST
def register_process(request):
    # Assuming the form data contains 'username', 'email', and 'password'
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Check if the username is available (optional)
    if User.objects.filter(username=username).exists():
        return HttpResponse("Username already taken.")

    # Create a new user object
    new_user = User.objects.create_user(username=username, email=email, password=password)

    # Log in the new user
    login(request, new_user)

    return redirect("/feed/")


@require_POST
def logout_process(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Log out the user
        logout(request)
        return redirect('/main/')
    else:
        return HttpResponse("You are not logged in.")


def feed(request):
    if request.user.is_authenticated:
        return render(request, "feed.html", context={'posts': get_posts()})
    else:
        return redirect('/login-page/')

@require_POST
def create_post_process(request):
    if request.user.is_authenticated:
        post_creator(content=request.POST['content'], request=request)
        return redirect("/feed/")
    else:
        return redirect("/login-page/")

@require_POST
def like_post(request, id):
    if request.user.is_authenticated:
        put_like(id, request)
        return HttpResponse("ok", status=200)


def like_analytics(request):
    from datetime import datetime
    from django.db.models import Count
    from .models import Like
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')

    date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
    date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()

    likes_data = Like.objects.filter(date__date__gte=date_from, date__date__lte=date_to) \
        .annotate(day=Count('date__date')) \
        .values('day') \
        .annotate(likes_count=Count('id')) \
        .values('day', 'likes_count')

    return JsonResponse(list(likes_data), safe=False)