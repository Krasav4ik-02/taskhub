# Generated by Django 3.2.19 on 2024-05-20 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_alter_user_bin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='task_goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='task_norm',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='task_plan',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', models.TextField(verbose_name=' Описание компаний')),
                ('email', models.CharField(max_length=30, verbose_name='Электронная почта')),
                ('address', models.CharField(max_length=30, verbose_name=' Адрес')),
                ('contact_phone', models.CharField(max_length=30, verbose_name=' Контактные данные')),
                ('telegram', models.CharField(max_length=30, verbose_name='Телеграмм')),
                ('bin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
