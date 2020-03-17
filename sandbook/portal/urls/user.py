from django.urls import path
from portal.views import user

user_urlpatterns = [
    path('user/<int:user_id>/', user.Index.as_view(), name='user_index'),
    path('user/<int:user_id>/', user.Profile.as_view(), name='user_profile'),
    path('user/<int:user_id>/circle/', user.Circle.as_view(), name='user_circle'),
    path('user/<int:user_id>/works/', user.Works.as_view(), name='user_works'),

    path('user/<int:user_id>/follow/', user.Follow.as_view(), name='user_follow'),
]
