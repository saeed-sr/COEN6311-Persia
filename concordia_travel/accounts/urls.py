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
    # path('agent_dashboard/bookings/<int:package_id>/', views.booking_detail, name='agent_booking_detail'),
    path('agent_dashboard/bookings/flight/<int:flight_id>/', views.flight_booking_detail, name='agent_flight_booking_detail'),
    path('agent_dashboard/bookings/hotel/<int:hotel_id>/', views.hotel_booking_detail, name='agent_hotel_booking_detail'),
    path('agent_dashboard/bookings/activity/<int:activity_id>/', views.activity_booking_detail, name='agent_activity_booking_detail'),
    path('agent_dashboard/bookings/premade_package/<int:package_id>/', views.premade_package_booking_detail, name='agent_premade_package_booking_detail'),



    ]