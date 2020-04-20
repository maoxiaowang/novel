import datetime

from django.utils import timezone
from django.views.generic.base import View, TemplateView

from base.models import Novel


class Index(TemplateView):
    template_name = 'portal/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            latest_novels=Novel.objects.select_related(
                'sub_category__category').order_by('-updated_at'))
        return context
