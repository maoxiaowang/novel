from base.constants.novel import BUILTIN_CATEGORIES
from base.models.account import Notification


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
    return context
