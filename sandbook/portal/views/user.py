from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from base.constants.account import SYSTEM_ROBOT_ID
from base.constants.novel import ALL_CATEGORIES
from base.models import User, ActivityLikes, ActivityComment
from general.views import JSONDetailView, JSONResponseMixin


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




# class BeAuthor()
#
#
