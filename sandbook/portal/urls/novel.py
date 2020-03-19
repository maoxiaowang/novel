from django.urls import path

from portal.views import novel

novel_urlpatterns = [
    path('novel/create/', novel.NovelCreate.as_view(), name='novel_create'),
]
