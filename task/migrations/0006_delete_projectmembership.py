# Generated by Django 3.2.19 on 2024-04-07 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_projectmembership'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectMembership',
        ),
    ]