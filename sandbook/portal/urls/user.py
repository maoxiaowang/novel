from django.urls import path
from portal.views import user

user_urlpatterns = [
    path('user/<int:user_id>/', user.HomePage.as_view(), name='user_homepage'),

    path('user/<int:user_id>/profile/', user.Profile.as_view(), name='user_profile_tab'),
    path('user/<int:user_id>/circle/', user.Circle.as_view(), name='user_circle_tab'),
    path('user/<int:user_id>/works/', user.Works.as_view(), name='user_works_tab'),

    path('user/<int:user_id>/follow/', user.Follow.as_view(), name='user_follow'),

    path('user/be-author/', user.BeAuthor.as_view(), name='user_be_author')

]
