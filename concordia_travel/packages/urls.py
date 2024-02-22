from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', views.flight_detail, name='flight_detail'),
    path('flights/book/<int:pk>/', views.book_flight, name='book_flight'),

    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/book/<int:pk>/', views.book_flight, name='book_hotel'),

    path('activities/', views.ActivityListView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', views.activity_detail, name='activities_detail'),
    path('activities/book/<int:pk>/', views.book_flight, name='book_activity'),
    # Add more URL patterns for detail views, create views, etc.
]
