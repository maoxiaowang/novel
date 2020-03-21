from django.db.transaction import non_atomic_requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from base.models import Novel
from portal.forms.novel import NovelCreationForm


class NovelCreate(CreateView):
    model = Novel
    form_class = NovelCreationForm
    template_name = 'portal/novel/blocks/create_form.html'

    @method_decorator(non_atomic_requests)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return render(self.request, 'portal/user/blocks/works.html')
