from django.db import models
from manager.models import *

class VacationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    date = models.DateField()
    comments = models.TextField()
    status = models.IntegerField( choices=((1, 'На согласований'),
                                                (2, 'Одобрено'),
                                                (3, 'Отклонено'),
                                                (4, 'Отозван'),), default=1)
    type_vacation = models.IntegerField( choices=((1, 'Ежегодный оплачиваемый'),
                                                  (2, 'Социальный'),
                                                  (5, 'Без содержания')))
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_vacation_requests')