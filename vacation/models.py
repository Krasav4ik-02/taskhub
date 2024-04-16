from django.db import models
from manager.models import *

class VacationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=(('pending', 'На рассмотрении'),
                                                      ('approved', 'Одобрено'),
                                                      ('rejected', 'Отклонено')), default='pending')
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_vacation_requests')