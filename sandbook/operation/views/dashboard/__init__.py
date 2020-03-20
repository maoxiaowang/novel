from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from base.constants.account import MANAGEMENT_GROUP_IDS


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'operations/dashboard/index.html'
    login_url = reverse_lazy('operation:account_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
