from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps 
from django.conf import settings
from celery._state import _set_current_app




# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prettyboy.settings')

app = Celery('prettyboy')

app.config_from_object(settings, namespace='CELERY')

_set_current_app(app)



# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.


app.config_from_object('django.conf:settings', namespace='CELERY')
#app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
app.autodiscover_tasks()
# Load task modules from all registered Django app configs.


#

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
