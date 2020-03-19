from django.urls import path

from portal.views import Index
from portal.urls.account import account_urlpatterns
from portal.urls.user import user_urlpatterns
from portal.urls.novel import novel_urlpatterns

app_name = 'portal'

urlpatterns = [
    path('', Index.as_view(), name='index')
]

urlpatterns += account_urlpatterns
urlpatterns += user_urlpatterns
urlpatterns += novel_urlpatterns
