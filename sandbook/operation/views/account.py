from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from operation.forms.account import AuthenticationForm


class Login(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = 'operations/account/login.html'
    # redirect_authenticated_user = True
    success_url = reverse_lazy('operation:dashboard_index')
    extra_context = {'redirect_field_name': 'next'}


class Logout(auth_views.LogoutView):
    pass
