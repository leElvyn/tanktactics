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
            background_task.models.Task.objects.filter(task_name='map.tasks.check_action_day').delete()
            tasks.check_action_day(repeat=5)
            subprocess.Popen(shlex.split(f"python {os.getcwd()}/manage.py process_tasks"))
