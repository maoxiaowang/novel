from operation.urls.account import auth_urlpatterns
from operation.urls.dashboard import dashboard_urlpatterns

app_name = 'operation'

urlpatterns = []

urlpatterns += auth_urlpatterns
urlpatterns += dashboard_urlpatterns
