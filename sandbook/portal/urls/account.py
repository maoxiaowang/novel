from django.urls import path
from django.views.generic import TemplateView

from portal.views import account

account_urlpatterns = [
    path('account/is-login/', account.IsLogin.as_view(), name='account_is_login'),
    path('account/login/', account.Login.as_view(), name='account_login'),
    path('account/logout/', account.Logout.as_view(), name='account_logout'),
    path('account/sign-up/', account.SignUp.as_view(), name='account_signup'),
    path('account/sign-up-done/', TemplateView.as_view(template_name='portal/account/signup_done.html'),
         name='account_signup_done'),
    path('account/active/<str:uidb64>/<str:token>/', account.Active.as_view(), name='account_active'),

    # 密码找回
    path('account/password/recover/', account.PasswordRecover.as_view(), name='account_password_recover'),
    path('account/password/recover-done/', TemplateView.as_view(
        template_name='portal/account/password/recover_done.html'), name='account_password_recover_done'),

    # 通过密码找回链接重置
    path('account/password/reset-confirm/<str:uidb64>/<str:token>/', account.PasswordResetConfirm.as_view(),
         name='account_password_reset_confirm'),
    path('account/password/reset-confirm-done/', TemplateView.as_view(
        template_name='portal/account/password/reset_confirm_done.html'),
         name='account_password_reset_confirm_done'),

]
