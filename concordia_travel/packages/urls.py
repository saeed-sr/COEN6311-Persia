from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', views.flight_detail, name='flight_detail'),
    path('flights/book/<int:pk>/', views.book_flight, name='book_flight'),
    path('flights/create/', views.add_flight, name='add_flight'),

    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/book/<int:pk>/', views.book_hotel, name='book_hotel'),
    path('hotels/create/', views.add_hotel, name='add_hotel'),


    path('activities/', views.ActivityListView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/book/<int:pk>/', views.book_activity, name='book_activity'),
    path('activities/create/', views.add_activity, name='add_activity'),


    path('custom-packages/create/', views.create_custom_package, name='create_custom_package'),
    path('custom-packages/<int:pk>/', views.CustomPackageDetailView.as_view(), name='custom-package-detail'),

    path('premade_packages/', views.PremadePackageListView.as_view(), name='premade_packages'),
    path('premade_packages/create/', views.add_premade_package, name='add_premade_package'),


    path('ask-question/<int:package_id>/', views.ask_question, name='ask_question'),

    path('premade_packages/book/<int:pk>/', views.book_premade_package, name='book_premade_package'),

    # Add more URL patterns for detail views, create views, etc.
]
