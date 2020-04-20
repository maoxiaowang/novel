from base.constants.novel import BUILTIN_CATEGORIES
from base.models.account import Notification
from django.conf import settings


def common(request):
    context = dict()
    context['builtin_categories'] = BUILTIN_CATEGORIES
    context['ID'] = '00000000'
    context['STR'] = 'XXXXXXXX'
    if request.user.is_authenticated:
        # notifications
        # fixme: 性能
        notifications = Notification.objects.filter(receiver=request.user)
        context['notifications'] = notifications

    context['default_avatar_url'] = settings.MEDIA_URL + 'default/avatars/user.jpg'
    return context
