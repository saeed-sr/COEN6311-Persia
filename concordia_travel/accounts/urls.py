from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    ]