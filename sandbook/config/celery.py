import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Only store task errors in the result backend.
app.conf.task_ignore_result = True
app.conf.task_store_errors_even_if_ignored = True

app.conf.task_time_limit = 1800

# 同一个 Worker 在执行了大量任务后，会有几率出现内存泄漏的情况。
# 这里建议全局设置 Worker 最大的任务执行数，Worker 在完成了最大的任务执行数后就主动退出
app.conf.worker_max_tasks_per_child = 100

# app.conf.worker_pool = 'gevent'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#daemonizing
