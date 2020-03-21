from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView, ListView

from base.constants.novel import CATEGORY_FANTASY_ID, NOVEL_STATUS_UNAPPROVED
from base.models import Category, Novel


class TaskIndex(LoginRequiredMixin, TemplateView):
    template_name = 'operations/dashboard/task/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.prefetch_related('subcategory_set')
        context.update(categories=categories)

        fantasy_category = Category.objects.get(id=CATEGORY_FANTASY_ID)
        fantasy_sub_categories = fantasy_category.subcategory_set.prefetch_related('novel_set')
        fantasy_unapproved_count = 0
        for sc in fantasy_sub_categories:
            sc_unapproved_count = sc.novel_set.filter(status=NOVEL_STATUS_UNAPPROVED).count()
            fantasy_unapproved_count += sc_unapproved_count
        context.update(fantasy_unapproved_count=fantasy_unapproved_count)

        return context


class TaskList(LoginRequiredMixin, ListView):
    template_name = 'operations/dashboard/task/list.html'
    model = Novel

    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=self.kwargs['category_id'])
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            sub_category__category=self.category,
            status=NOVEL_STATUS_UNAPPROVED
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(category=self.category)
        return context
