from django.urls import path
from . import views

urlpatterns = [
    # ... your other url patterns ...
    path('<int:booking_id>/', views.payment, name='payment_process'),
]