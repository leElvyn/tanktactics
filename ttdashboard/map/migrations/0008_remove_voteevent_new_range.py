# Generated by Django 3.2.6 on 2023-05-17 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_voteevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voteevent',
            name='new_range',
        ),
    ]
