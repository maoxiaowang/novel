from django.urls import path

from operation.views import account

auth_urlpatterns = [
    path('login/', account.Login.as_view(), name='account_login'),
    path('logout/', account.Logout.as_view(), name='account_logout')
]
