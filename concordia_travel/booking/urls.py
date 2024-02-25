from django.urls import path
from . import views



urlpatterns = [
    path('book/', views.book_custom_package, name='book_custom_package'),
    # Add more URL patterns as needed
]
