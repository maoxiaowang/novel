from django.contrib import messages
from django.views.generic import ListView, UpdateView

from base.models import AuthorApplication, AuthorInfo
from general.views import JSONResponseMixin


class ApplicationList(ListView):
    model = AuthorApplication
    template_name = 'operations/dashboard/application/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(status=AuthorApplication.STATUS['unapproved'])


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
        # AuthorInfo.objects.create(user=form.instance.applier, name=)

        if form.cleaned_data['status'] == AuthorApplication.STATUS['agreed']:
            messages.add_message(self.request, messages.SUCCESS, '已同意用户“%s”的申请'
                                 % form.instance.applier.username)
        elif form.cleaned_data['status'] == AuthorApplication.STATUS['rejected']:
            messages.add_message(self.request, messages.SUCCESS, '已拒绝用户“%s”的申请'
                                 % form.instance.applier.username)
        return self.json_response()
