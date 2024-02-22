from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('activities/', views.ActivityListView.as_view(), name='activity-list'),
    # Add more URL patterns for detail views, create views, etc.
]
