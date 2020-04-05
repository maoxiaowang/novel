from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View

from base.constants.account import SYSTEM_ROBOT_ID
from base.constants.novel import ALL_CATEGORIES
from base.models import User, ActivityLikes, ActivityComment, Novel, AuthorApplication
from general.views import JSONResponseMixin


class HomeBaseView(LoginRequiredMixin, DetailView):
    model = User
    pk_url_kwarg = 'user_id'


class HomePage(HomeBaseView):
    """
    用户主页

    非自己的主页，只能看到当前用户的动态（若未开启隐私保护）
    自己的主页，可以看到自己和自己关注的人（非对方黑名单或隐私保护）的动态

    发送私信（非自己主页）
    关注/取消关注（非自己主页）

    """
    template_name = 'portal/user/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(categories=ALL_CATEGORIES)
        return context


class Profile(HomeBaseView):
    """
    个人资料
    """
    template_name = 'portal/user/blocks/profile.html'


class Circle(HomeBaseView):
    """
    用户圈子
    """
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


class Settings(HomeBaseView):
    """
    用户（账号）设置
    """
    template_name = 'portal/user/blocks/settings.html'


class Works(HomeBaseView):
    """
    用户（作家）的作品管理
    """
    template_name = 'portal/user/blocks/works.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_author:
            works = self.object.novel_set.select_related(
                'sub_category__category').prefetch_related('volume_set__chapter_set')
            context.update(works=works)

        # if be-author application exists
        context.update(
            application=AuthorApplication.objects.filter(
                applier=self.request.user, status=AuthorApplication.STATUS['unapproved']).exists()
        )
        return context


class Follow(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    """
    关注/取消关注
    """
    ...


class NovelDetail(DetailView):
    model = Novel


class BeAuthor(JSONResponseMixin, View):
    """
    创建审批
    """
    http_method_names = ['post']

    def post(self, request, **kwargs):
        if not request.user.is_author:
            AuthorApplication.objects.get_or_create(
                defaults={'applier': request.user}, applier=request.user,
                status=AuthorApplication.STATUS['unapproved']
            )
            return self.json_response()
        return self.json_response(result=False)

