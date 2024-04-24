from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("search/", views.search, name='search'),
    path('error/', views.error_page, name='error_page'),  # Ensure this view exists
]
