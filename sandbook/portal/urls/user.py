from django.urls import path
from portal.views import user

user_urlpatterns = [
    path('user/<int:user_id>/', user.Home.as_view(), name='user_home'),
    path('user/<int:user_id>/<slug:part>/', user.HomePart.as_view(), name='user_home_part'),

    # path('user/<int:user_id>/profile/', user.Profile.as_view(), name='user_profile_tab'),
    # path('user/<int:user_id>/circle/', user.Circle.as_view(), name='user_circle_tab'),
    # path('user/<int:user_id>/works/', user.Works.as_view(), name='user_works_tab'),
    # path('user/<int:user_id>/settings/', user.Settings.as_view(), name='user_settings_tab'),
    path('user/<int:user_id>/follow/', user.Follow.as_view(), name='user_follow'),

    path('user/become-author/', user.BecomeAuthor.as_view(), name='user_become_author')

]
