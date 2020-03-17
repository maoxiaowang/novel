from django.views.generic import DetailView, UpdateView

from base.models import User
from general.views import JSONDetailView, JSONResponseMixin


class Index(DetailView):
    """
    用户主页

    非自己的主页，只能看到当前用户的动态（若未开启隐私保护）
    自己的主页，可以看到自己和自己关注的人（非对方黑名单或隐私保护）的动态

    发送私信（非自己主页）
    关注/取消关注（非自己主页）

    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class Profile(JSONResponseMixin, DetailView):
    """
    个人资料
    """
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'user/blocks/profile.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return self.json_response(data={'html': response})


class Circle(DetailView):
    """
    用户圈子
    """
    ...


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
    template_name = 'user/works.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_author:
            ...

        return context


class Follow(JSONResponseMixin, UpdateView):
    """
    关注/取消关注
    """
    ...




# class BeAuthor()
#
#
