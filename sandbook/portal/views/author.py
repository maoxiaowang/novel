from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View

from base.models import Novel, Chapter, AuthorApplication
from general.views import JSONResponseMixin
from portal.forms.novel import NovelCreationForm, ChapterUpdateForm, ChapterCreateForm


class NovelCreate(CreateView):
    model = Novel
    form_class = NovelCreationForm
    template_name = 'portal/user/blocks/novel/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return render(self.request, 'portal/user/blocks/works.html')


class NovelUpdate(LoginRequiredMixin, UpdateView):
    """
    作家小说更新页面
    列出所有章节标题
    """
    model = Novel
    pk_url_kwarg = 'novel_id'
    form_class = ChapterUpdateForm
    template_name = 'portal/user/blocks/novel/update_page.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != request.user:
            raise PermissionDenied
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter_id = self.kwargs.get('cid', 1)
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            pass
        else:
            context.update(chapter=chapter)
            context.update(form=self.form_class(
                initial={'title': chapter.title, 'content': chapter.content}
            ))
        return context


class ChapterCreate(CreateView):
    model = Chapter
    form_class = ChapterCreateForm
    pk_url_kwarg = 'novel_id'
    http_method_names = ['post']

    def get_success_url(self):
        return reverse(
            'portal:novel_update', kwargs={'novel_id': self.object.novel.id}
        ) + '?chapter=%s' % self.object.id
