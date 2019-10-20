from celery import Celery

from project.settings.utils import load_settings

load_settings()

app = Celery('bitbucket_github')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
