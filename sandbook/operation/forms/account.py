from django import forms
from django.contrib.auth.forms import UsernameField


from django.contrib.auth import forms as auth_forms, password_validation


class AuthenticationForm(auth_forms.AuthenticationForm):
    """
    For extending
    """
    username = UsernameField(
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'min_length': 6,
                'max_length': 32,
                'class': 'form-control'
            },
        )
    )
    password = forms.CharField(
        label='密码',
        label_suffix='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                # 'autocomplete': 'current-password',
                'class': 'form-control'
            }
        ),
    )
    remember_me = forms.BooleanField(
        label='保持登录',
        label_suffix='',  # remove ':'
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox',
                'name': 'remember_me'
            }
        ),
        required=False,
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.error_messages.update()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # 机器人不能登陆，非管理员不能登陆
        if user.is_robot or not user.is_manager:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
