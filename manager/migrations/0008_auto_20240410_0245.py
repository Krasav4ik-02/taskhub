# Generated by Django 3.2.19 on 2024-04-09 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_alter_user_data_joined_to_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.CharField(max_length=30, null=True),
        ),
    ]