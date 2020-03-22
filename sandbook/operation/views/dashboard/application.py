from django.views.generic import ListView, UpdateView

from base.models import AuthorApplication
from general.views import JSONResponseMixin


class ApplicationList(ListView):
    model = AuthorApplication
    template_name = 'operations/dashboard/application/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(status=AuthorApplication.STATUS_UNAPPROVED)


class ApplicationApprove(JSONResponseMixin, UpdateView):
    """
    同意或拒绝（成为作家）
    """
    model = AuthorApplication
    http_method_names = ['post']
    fields = ('status',)

    def form_valid(self, form):
        form.instance.approver = self.request.user
        form.save()
        return self.json_response()
