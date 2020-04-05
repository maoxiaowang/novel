from django.urls import path

from portal.views import author

author_urlpatterns = [
    path('author/novel/create/', author.NovelCreate.as_view(), name='novel_create'),
    # （作品管理）
    path('author/novel/<int:novel_id>/chapter/<int:chapter_id>/',
         author.ChapterUpdate.as_view(), name='novel_chapter_update'),
    path('author/novel/volume/create/', author.VolumeCreate.as_view(),
         name='novel_volume_create'),
    path('author/novel/volume/<int:volume_id>/rename/', author.VolumeRename.as_view(),
         name='novel_volume_rename'),
    path('author/novel/chapter/create/', author.ChapterCreate.as_view(),
         name='novel_chapter_create'),

]
