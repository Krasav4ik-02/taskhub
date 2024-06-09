from django.urls import path
from . import views

urlpatterns = [
    path('vacation', views.calculate_vacation_days, name='vacation'),
    path('vacations_for_manager' , views.vacations_for_manager, name='vacations_for_manager'),
    path('submit_vacation' , views.submit_vacation, name='submit_vacation'),
    path('apply_vacation' , views.apply_vacation, name='apply_vacation'),
    path('reject_vacation' , views.reject_vacation, name='reject_vacation'),
    path('vacations_for_manager_apply' , views.vacations_for_manager_apply, name='vacations_for_manager_apply'),
    path('vacations_for_manager_reject' , views.vacations_for_manager_reject, name='vacations_for_manager_reject'),
    path('vacation_tasks' , views.vacation_tasks, name='vacation_tasks'),
    path('recall_vacation' , views.recall_vacation, name='recall_vacation'),
    path('vacations_for_manager_recall' , views.vacations_for_manager_recall, name='vacations_for_manager_recall'),
    path('edit_vacation' , views.edit_vacation, name='edit_vacation'),
]
