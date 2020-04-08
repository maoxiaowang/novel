from django.views.generic import CreateView, DetailView, ListView

from base.models import Novel, Chapter, NovelComment
from general.forms.mixin import FormValidationMixin
from general.views.mixin import LoginRequiredMixin
from portal.forms.novel import NovelCommentCreateForm


class NovelDetail(DetailView):
    model = Novel
    pk_url_kwarg = 'novel_id'
    template_name = 'portal/novel/detail.html'
    context_object_name = 'novel'


class NovelChapterDetail(DetailView):
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    template_name = 'portal/novel/chapter_detail.html'
    context_object_name = 'chapter'


class NovelCommentList(ListView):
    """
    整个评论列表，分页
    """
    model = NovelComment
    template_name = 'portal/novel/blocks/comment_area.html'
    paginate_by = 5
    ordering = ('-created_at',)

    def get_queryset(self):
        self.novel = Novel.objects.get(id=self.kwargs['novel_id'])
        novel_comments = self.novel.novelcomment_set
        self.comment_count = novel_comments.count()
        return novel_comments.order_by(*self.ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(novel=self.novel, comment_counts=self.comment_count)
        return context


class NovelCommentCreate(LoginRequiredMixin, FormValidationMixin, CreateView):
    model = NovelComment
    form_class = NovelCommentCreateForm
    pk_url_kwarg = 'novel_id'
    template_name = 'portal/novel/blocks/comment_area.html'
    context_object_name = 'novel'

    def form_valid(self, form):
        novel = Novel.objects.get(id=self.kwargs['novel_id'])
        form.instance.novel = novel
        form.instance.user = self.request.user
        form.save()
        return self.render_to_response({'novel': novel})
