from django.apps import AppConfig
import subprocess
import os
import shlex
import background_task
import sys

class MapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map'
    def ready(self):
        if sys.argv[1] == 'runserver':
            from map import tasks
            background_task.models.CompletedTask.objects.all().delete()
            subprocess.Popen(shlex.split(f"python {os.getcwd()}/manage.py process_tasks"))
