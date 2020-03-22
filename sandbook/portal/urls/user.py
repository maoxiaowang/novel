from django.urls import path
from portal.views import user

user_urlpatterns = [
    path('user/<int:user_id>/', user.HomePage.as_view(), name='user_homepage'),

    path('user/<int:user_id>/profile/', user.Profile.as_view(), name='user_profile_tab'),
    path('user/<int:user_id>/circle/', user.Circle.as_view(), name='user_circle_tab'),
    path('user/<int:user_id>/works/', user.Works.as_view(), name='user_works_tab'),

    path('user/<int:user_id>/follow/', user.Follow.as_view(), name='user_follow'),

    path('user/novel/create/', user.NovelCreate.as_view(), name='novel_create'),
    # （作品管理）
    path('user/novel/<int:novel_id>/update/', user.NovelUpdate.as_view(),
         name='user_novel_update'),
    path('user/novel/<int:novel_id>/chapter/create/', user.ChapterCreate.as_view(), name='user_novel_chapter_create'),

]
