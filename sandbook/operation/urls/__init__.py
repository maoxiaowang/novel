from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from operation.urls.account import auth_urlpatterns
from operation.views.dashboard import Index

app_name = 'operation'

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index')
]

urlpatterns += auth_urlpatterns
