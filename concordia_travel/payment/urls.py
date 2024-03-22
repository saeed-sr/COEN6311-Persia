from django.urls import path
from . import views

urlpatterns = [
    # ... your other url patterns ...
    path('<int:booking_id>/', views.payment, name='payment_process'),

    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
]