# Generated by Django 3.2.19 on 2024-04-04 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20240404_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_date_status',
        ),
    ]
