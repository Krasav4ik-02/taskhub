import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Manager(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    bin = models.CharField(verbose_name='БИН Компании', max_length=30)
    name = models.CharField( verbose_name='Название Компании', max_length=255)

class Invintation(models.Model):
    company = models.ForeignKey(Manager, on_delete=models.CASCADE)
    invitation_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invite_link = models.URLField()

    def get_absolute_url(self):
        return reverse('register_link', args=[str(self.invite_code)])



