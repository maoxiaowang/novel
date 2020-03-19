from django import forms
from django.contrib.auth import forms as auth_forms, password_validation
from django.contrib.auth.forms import UsernameField
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from base.models.account import User
from base.tasks import async_send_email


class AuthenticationForm(auth_forms.AuthenticationForm):
    """
    For extending
    """
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'min_length': 6,
                'max_length': 32,
                'placeholder': '用户名',
                'class': 'form-control'
            },
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': '密码',
                'class': 'form-control'
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.error_messages.update()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # 机器人不能登陆
        if user.is_robot:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )


class SignUpForm(auth_forms.UserCreationForm):
    # terms_and_conditions = forms.BooleanField(
    #     label_suffix='',
    #     label=_('I agree to the %(term)s') % {
    #         'term': mark_safe('<a href="#" data-toggle="modal" data-target="#terms-conditions-modal">'
    #                           '%s</a>' % _('terms and conditions'))
    #     },
    #     widget=forms.CheckboxInput({
    #         'class': 'custom-control-label',
    #         'id': 'terms-checkbox'
    #     })
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label_suffix = ''
        self.fields['username'].help_text = _('Username is the only identifier of your account.')
        self.fields['password1'].label_suffix = ''
        self.fields['password1'].help_text = password_validation.password_validators_help_texts()
        self.fields['password2'].label_suffix = ''
        self.fields['email'].label_suffix = ''
        self.fields['email'].help_text = _('Email address is important to active and your account '
                                           'and help to recover password.')
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '密码',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '确认密码',
        })

    def save(self, commit=True):
        # initial active status is False
        self.instance.is_active = False
        return super().save(commit=commit)

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '用户名',
                    'required': True,
                    'spellcheck': 'false',
                    'autofocus': True,
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': '电子邮件'
                }
            ),
        }


class ActiveForm(forms.Form):
    user_pk = forms.IntegerField()

    def get_user(self, user_pk):
        return User.objects.get(pk=user_pk)

    def save(self):
        user = self.get_user(self.cleaned_data['user_pk'])
        user.is_active = True
        user.save()


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label='电子邮件',
        label_suffix='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'autofocus': True,
            }
        ),
        max_length=254,
        help_text='输入与你的账号关联的Email地址'
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and not User.objects.filter(email=email).exists():
            raise forms.ValidationError('此邮件地址未被注册')
        return email

    def get_users(self, email):
        active_users = User.objects.filter(**{
            '%s__exact' % User.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        html_context = {
            'subject': subject, 'content': body, 'date': context.get('date')
        }

        html_message = loader.render_to_string(html_email_template_name, html_context)
        async_send_email.delay(subject, html_message, [to_email])


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label='新密码',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autofocus': True,
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='新密码确认',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
        strip=False,
    )
