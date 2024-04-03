from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('update_question/<int:question_id>/', views.update_question, name='update_question'),
    path('agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
    ]