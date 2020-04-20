from django.urls import path

from portal.views import novel

novel_urlpatterns = [
    path('novel/<int:novel_id>/', novel.NovelDetail.as_view(), name='novel_detail'),
    path('novel/chapter/<int:chapter_id>/', novel.NovelChapterDetail.as_view(), name='novel_chapter_detail'),

    # comment
    path('novel/<int:novel_id>/comment/create/', novel.NovelCommentCreate.as_view(), name='novel_comment_create'),
    path('novel/<int:novel_id>/comment/list/', novel.NovelCommentList.as_view(), name='novel_comment_list'),
    path('novel/comment/<int:pk>/reply/list/', novel.NovelCommentReplyList.as_view(),
         name='novel_comment_reply_list'),
    path('novel/comment/<int:pk>/reply/create/', novel.NovelCommentReplyCreate.as_view(),
         name='novel_comment_reply_create'),
]
