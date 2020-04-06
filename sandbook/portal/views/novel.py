from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.transaction import non_atomic_requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from base.models import Novel
from portal.forms.novel import NovelCreationForm


class NovelDetail(DetailView):
    model = Novel
    pk_url_kwarg = 'novel_id'
    template_name = ''
    context_object_name = 'novel'
