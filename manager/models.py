import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    bin = models.CharField(verbose_name='БИН Компании', max_length=12, null=False)
    name_company = models.CharField( verbose_name='Название Компании', max_length=255, null=False)
    role = models.IntegerField(choices=((1, 'Manager'),
                                        (2, 'Developer Junior'),
                                        (3, 'Developer Middle'),
                                        (4, 'Developer Senior'),
                                        (5, 'Developer Teamlead'),
                                        (6, 'Tester'),
                                        (7, 'Analyst'),
                                        (8, 'Main Analyst')), default=1, null=False)
    data_joined_to_work = models.DateField(null=True)







