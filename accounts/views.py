from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def csrf_view(request):
    # Ensures the CSRF cookie is set for the React app
    return JsonResponse({'ok': True})


def signup_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'ok': True, 'message': 'Already signed in.'})

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'message': 'Method not allowed.'}, status=405)

    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '').strip()

    if not email or not password:
        return JsonResponse({'ok': False, 'message': 'Email and password are required.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'ok': False, 'message': 'User with this email already exists.'}, status=400)

    username = email.split('@')[0]
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return JsonResponse({'ok': True, 'message': 'Account created.'})


def signin_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'ok': True, 'message': 'Already signed in.'})

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'message': 'Method not allowed.'}, status=405)

    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '').strip()
    db_user = User.objects.filter(email=email).first()
    if db_user:
        user = authenticate(request, username=db_user.username, password=password)
    else:
        user = None

    if user is not None:
        login(request, user)
        return JsonResponse({'ok': True, 'message': 'Signed in.'})

    return JsonResponse({'ok': False, 'message': 'Invalid email or password.'}, status=400)


def success_view(request):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:5173')
    accept = request.headers.get('Accept', '')

    if not request.user.is_authenticated:
        if 'text/html' in accept:
            return redirect(f'{frontend_url}/?unauthorized=1')
        return JsonResponse({'ok': False, 'message': 'Not authenticated.'}, status=401)

    if 'text/html' in accept:
        return redirect(f'{frontend_url}/?success=1')

    user = request.user
    return JsonResponse({'ok': True, 'user': {'username': user.username, 'email': user.email}})


def logout_view(request):
    logout(request)
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:5173')
    return redirect(f'{frontend_url}/?logged_out=1')
