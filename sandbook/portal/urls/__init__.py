from django.urls import path
from django.views.generic import TemplateView

from portal.views import Index
from portal.urls.account import account_urlpatterns
from portal.urls.user import user_urlpatterns
from portal.urls.novel import novel_urlpatterns
from portal.urls.author import author_urlpatterns

app_name = 'portal'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('test/', TemplateView.as_view(template_name='test.html'))
]

urlpatterns += account_urlpatterns
urlpatterns += user_urlpatterns
urlpatterns += novel_urlpatterns
urlpatterns += author_urlpatterns
