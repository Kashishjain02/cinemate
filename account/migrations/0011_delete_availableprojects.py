# Generated by Django 4.1.6 on 2023-07-09 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_availableprojects_location'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AvailableProjects',
        ),
    ]
