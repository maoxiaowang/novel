from django.shortcuts import render
from django.views.generic import CreateView

from base.models import Novel
from portal.forms.novel import NovelCreationForm


class NovelCreate(CreateView):
    model = Novel
    form_class = NovelCreationForm
    template_name = 'portal/novel/blocks/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return render(self.request, 'portal/user/blocks/works.html')
