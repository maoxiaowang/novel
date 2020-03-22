from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, CreateView, RedirectView

from base.constants.account import SYSTEM_ROBOT_ID
from base.constants.novel import ALL_CATEGORIES
from base.models import User, ActivityLikes, ActivityComment, Novel, Chapter
from general.views import JSONResponseMixin
from portal.forms.novel import NovelCreationForm, ChapterUpdateForm, ChapterCreateForm


class HomePage(DetailView):
    """
    用户主页

    非自己的主页，只能看到当前用户的动态（若未开启隐私保护）
    自己的主页，可以看到自己和自己关注的人（非对方黑名单或隐私保护）的动态

    发送私信（非自己主页）
    关注/取消关注（非自己主页）

    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'portal/user/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(categories=ALL_CATEGORIES)
        return context


class Profile(DetailView):
    """
    个人资料
    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'portal/user/blocks/profile.html'


class Circle(DetailView):
    """
    用户圈子
    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'portal/user/blocks/circle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = self.object.activity_set.prefetch_related(
            Prefetch('likes', queryset=ActivityLikes.objects.filter(user=self.object),
                     to_attr='user_likes'),
            Prefetch('comments', queryset=ActivityComment.objects.filter(user=self.object),
                     to_attr='user_comments')
        )
        context.update(activities=activities)
        context.update(system_robot=self.model.objects.get(id=SYSTEM_ROBOT_ID))
        return context


class Settings:
    """
    用户（账号）设置
    """
    ...


class Works(DetailView):
    """
    用户（作家）的作品管理
    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'portal/user/blocks/works.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_author:
            works = self.object.novel_set.prefetch_related('sub_category__category')
            context.update(works=works)
        return context


class Follow(JSONResponseMixin, UpdateView):
    """
    关注/取消关注
    """
    ...


class NovelCreate(CreateView):
    model = Novel
    form_class = NovelCreationForm
    template_name = 'portal/user/blocks/novel/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return render(self.request, 'portal/user/blocks/works.html')


class NovelDetail(DetailView):
    model = Novel


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


class ChapterCreate(JSONResponseMixin, CreateView):
    model = Chapter
    form_class = ChapterCreateForm
    pk_url_kwarg = 'novel_id'
    http_method_names = ['post']

    def get_success_url(self):
        return reverse(
            'portal:user_novel_update', kwargs={'novel_id': self.object.novel.id}
        ) + '?chapter=%s' % self.object.id

    def form_valid(self, form):
        self.object = form.save()
        return self.json_response(data={'url': self.get_success_url()})
