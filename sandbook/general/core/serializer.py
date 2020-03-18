import decimal
import json
import uuid
from datetime import datetime, date, time

from django.db.models import Model
from django.db.models.fields.files import FieldFile
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.functional import Promise


class SJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return timezone.localtime(obj).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return timezone.localdate(obj).strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, (decimal.Decimal, uuid.UUID, Promise)):
            return str(obj)
        elif obj.__class__.__name__ == 'GenericRelatedObjectManager':
            return
        elif isinstance(obj, FieldFile):
            if obj:
                return obj.url
        elif isinstance(obj, Model):
            return model_to_dict(obj, exclude=['password'])

        return super().default(obj)
