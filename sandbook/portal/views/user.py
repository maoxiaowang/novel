from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import DetailView, UpdateView, CreateView
from django.views.generic.base import View

from base.constants.account import SYSTEM_ROBOT_ID
from base.constants.novel import ALL_CATEGORIES
from base.models import User, ActivityLikes, ActivityComment, Novel, AuthorApplication
from general.forms.mixin import FormValidationMixin
from general.views import JSONResponseMixin
from portal.forms.user import AuthorApplicationForm


class Home(DetailView):
    """
    用户主页（领地）

    书架，信箱，通知，设置
    非本人只能看到书架菜单（可在设置中关闭书架里书）

    """
    model = User
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(categories=ALL_CATEGORIES)
        return context

    def get_template_names(self):
        if self.object == self.request.user:
            # 被访问用户是请求本人
            return ['portal/user/home/my_home.html']
        return ['portal/user/home/user_home.html']


class HomePart(DetailView):
    """
    用户主页其他部分
    """
    model = User
    pk_url_kwarg = 'user_id'
    parts = ('bookshelf', 'home', 'mailbox', 'settings', 'workbench')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = self.kwargs.get('part')
        try:
            context = self.__getattribute__('get_%s_context_data' % part)(context)
        except AttributeError:
            pass
        return context

    def get_template_names(self):
        part = self.kwargs.get('part')
        if part not in self.parts:
            raise Http404
        self.template_name = 'portal/user/home/parts/%s.html' % part
        return super().get_template_names()

    def get_bookshelf_context_data(self, context):
        return context

    def get_workbench_context_data(self, context):
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


# class Profile(HomeBaseView):
#     """
#     个人资料
#     """
#     template_name = 'portal/user/blocks/profile.html'
#
#
# class Circle(HomeBaseView):
#     """
#     用户圈子
#     """
#     template_name = 'portal/user/blocks/circle.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         activities = self.object.activity_set.prefetch_related(
#             Prefetch('likes', queryset=ActivityLikes.objects.filter(user=self.object),
#                      to_attr='user_likes'),
#             Prefetch('comments', queryset=ActivityComment.objects.filter(user=self.object),
#                      to_attr='user_comments')
#         )
#         context.update(activities=activities)
#         context.update(system_robot=self.model.objects.get(id=SYSTEM_ROBOT_ID))
#         return context
#
#
# class Settings(HomeBaseView):
#     """
#     用户（账号）设置
#     """
#     template_name = 'portal/user/blocks/settings.html'
#
#
# class Works(HomeBaseView):
#     """
#     用户（作家）的作品管理
#     """
#     template_name = 'portal/user/blocks/works.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.object.is_author:
#             works = self.object.novel_set.select_related(
#                 'sub_category__category').prefetch_related('volume_set__chapter_set')
#             context.update(works=works)
#
#         # if be-author application exists
#         context.update(
#             application=AuthorApplication.objects.filter(
#                 applier=self.request.user, status=AuthorApplication.STATUS['unapproved']).exists()
#         )
#         return context


class Follow(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    """
    关注/取消关注
    """
    ...


class NovelDetail(DetailView):
    model = Novel


class BecomeAuthor(FormValidationMixin, CreateView):
    """
    创建审批
    """
    model = AuthorApplication
    form_class = AuthorApplicationForm
    http_method_names = ['post']

    def form_valid(self, form):
        form.instance.applier = self.request.user
        # fixme: 暂时不需要审批
        # form.instance.status = AuthorApplication.STATUS['unapproved']
        form.instance.status = AuthorApplication.STATUS['agreed']
        return super().form_valid(form)
