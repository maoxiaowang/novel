import datetime

from django.utils import timezone
from django.views.generic.base import View, TemplateView

from base.models import Novel


class Index(TemplateView):
    template_name = 'portal/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            latest_novels=Novel.objects.filter(
                updated_at__gte=timezone.now() - datetime.timedelta(days=3),
                status=Novel.STATUS['active']
            ).order_by('-updated_at'))
        return context
