from django.urls import path
from . import views



urlpatterns = [
    path('book/', views.book_custom_package, name='book_custom_package'),

    path('view_bookings/', views.view_bookings, name='view_bookings'),

    path('complete_booking/<int:custom_package_id>/', views.complete_booking, name='complete_booking'),

    path('booking/detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),

    path('share_your_experience/', views.share_your_experience, name='share_your_experience'),

    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

]
