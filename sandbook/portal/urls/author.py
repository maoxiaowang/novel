from django.urls import path

from portal.views import author

author_urlpatterns = [
    path('author/novel/create/', author.NovelCreate.as_view(), name='novel_create'),
    # （作品管理）
    path('author/novel/<int:novel_id>/update/', author.NovelUpdate.as_view(),
         name='novel_update'),
    path('author/novel/<int:novel_id>/chapter/create/', author.ChapterCreate.as_view(),
         name='novel_chapter_create'),

]
