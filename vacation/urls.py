from django.urls import path
from . import views

urlpatterns = [
    path('vacation', views.calculate_vacation_days, name='vacation'),
]