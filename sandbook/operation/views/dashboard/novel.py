from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.generic import ListView, UpdateView

from base.models import Novel, Category
from operation.models import OperationLog


class NovelList(ListView):
    """
    按类别过滤的小说列表
    """
    model = Novel
    template_name = 'operations/dashboard/novel/list.html'
    category = None

    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=self.kwargs['category_id'])
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(sub_category__category=self.category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(category=self.category)
        return context


class UpdateStatus(UpdateView):
    model = Novel
    pk_url_kwarg = 'novel_id'
    fields = ('status',)

    def form_valid(self, form):
        self.object = form.save()
        OperationLog.objects.create(
            manager=self.request.user, novel=self.object,
            action='更改作品状态至 %s' % self.object.get_status_display()
        )
        messages.add_message(self.request, messages.SUCCESS, '操作成功')
        return HttpResponse()
