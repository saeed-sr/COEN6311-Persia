from django.urls import path
from . import views



urlpatterns = [
    path('book/', views.book_custom_package, name='book_custom_package'),

    path('view_bookings/', views.view_bookings, name='view_bookings'),

    path('complete_booking/<int:custom_package_id>/', views.complete_booking, name='complete_booking'),

    # Add more URL patterns as needed
]
