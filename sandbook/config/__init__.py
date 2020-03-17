from django.urls import register_converter
from django.urls.converters import IntConverter, StringConverter

#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import app as celery_app
#

__all__ = ['celery_app']

from .celery import app as celery_app

register_converter(IntConverter, 'int')
register_converter(StringConverter, 'str')
