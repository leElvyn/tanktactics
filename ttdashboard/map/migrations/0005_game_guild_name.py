# Generated by Django 3.2.6 on 2022-05-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_game_logs_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='guild_name',
            field=models.CharField(default='...', max_length=30, verbose_name='Guild Name'),
            preserve_default=False,
        ),
    ]
