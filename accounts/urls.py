from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.csrf_view, name='csrf'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('success/', views.success_view, name='success'),
    path('logout/', views.logout_view, name='logout'),
]
