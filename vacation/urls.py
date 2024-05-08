from django.urls import path
from . import views

urlpatterns = [
    path('vacation', views.calculate_vacation_days, name='vacation'),
    path('vacations_for_manager' , views.vacations_for_manager, name='vacations_for_manager'),
]
