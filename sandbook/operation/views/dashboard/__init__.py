from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from base.constants.account import MANAGEMENT_GROUP_IDS
from base.constants.novel import (
    CATEGORY_FANTASY_ID, NOVEL_STATUS_ACTIVE, NOVEL_STATUS_FINISHED, NOVEL_STATUS_UNAPPROVED)
from base.models import Novel, Category


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'operations/dashboard/index.html'
    login_url = reverse_lazy('operation:account_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fantasy_category = Category.objects.get(id=CATEGORY_FANTASY_ID)

        # init fantasy count
        all_fantasy_count = 0
        active_fantasy_count = 0
        finished_fantasy_count = 0
        unapproved_fantasy_count = 0
        fantasy_sub_categories = fantasy_category.subcategory_set.prefetch_related('novel_set')
        fantasy_category_list = list()
        for sc in fantasy_sub_categories:
            novels = sc.novel_set
            sc_novel_count = novels.count()
            fantasy_category_list.append(
                {'name': sc.name, 'count': sc_novel_count, }
            )
            all_fantasy_count += sc_novel_count
            active_fantasy_count += novels.filter(status=NOVEL_STATUS_ACTIVE).count()
            finished_fantasy_count += novels.filter(status=NOVEL_STATUS_FINISHED).count()
            unapproved_fantasy_count += novels.filter(status=NOVEL_STATUS_UNAPPROVED).count()
        # 添加百分比
        for item in fantasy_category_list:
            item['percent'] = round(item['count']*100 / all_fantasy_count, 1) if all_fantasy_count > 0 else 0
        # 按数量排序
        fantasy_category_list = sorted(fantasy_category_list, key=lambda c: c['count'], reverse=True)
        context.update(
            fantasy_sub_categories=fantasy_category_list,
            all_fantasy_count=all_fantasy_count,
            active_fantasy_count=active_fantasy_count,
            finished_fantasy_count=finished_fantasy_count,
            unapproved_fantasy_count=unapproved_fantasy_count
        )
        return context
