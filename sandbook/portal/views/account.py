from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, DetailView

from base.models.account import User
from general.forms.mixin import FormValidationMixin
from portal.forms.account import AuthenticationForm, SignUpForm, ActiveForm, PasswordResetForm, SetPasswordForm
from portal.tasks import send_user_creating_email

INTERNAL_ACTIVE_URL_TOKEN = 'account-active'
INTERNAL_ACTIVE_SESSION_TOKEN = '_account_active_token'


class Login(FormValidationMixin, auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        res = super().form_valid(form)
        return res


class Logout(auth_views.LogoutView):
    pass


class SignUp(FormValidationMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('portal:account_signup_done')
    valid_link = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # site = get_current_site(self.request)
        # send email to user
        send_user_creating_email.delay(
            [self.object.email],
            self.object.username,
            self.request.build_absolute_uri(
                reverse(
                    'portal:account_active',
                    kwargs={
                        'uidb64': urlsafe_base64_encode(force_bytes(self.object.pk)),
                        'token': default_token_generator.make_token(self.object)
                    }
                )
            ),
        )
        self.valid_link = True
        return response


class Active(FormView):
    valid_link = False
    user = None
    token_generator = default_token_generator
    form_class = ActiveForm
    success_url = reverse_lazy('client20:account_active_done')
    template_name = 'account/active_done.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_ACTIVE_URL_TOKEN:
                # active account
                session_token = self.request.session.get(INTERNAL_ACTIVE_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, active account
                    self.valid_link = True
                    return super().dispatch(request, *args, **kwargs)
            else:
                # save token in session, and redirect to account-active
                if self.token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_ACTIVE_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_ACTIVE_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        # treat the active link as a post request
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        # form is always valid
        # change is_active to True
        form.save()
        del self.request.session[INTERNAL_ACTIVE_SESSION_TOKEN]
        return self.render_to_response(self.get_context_data())

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), data={'user_pk': self.user.pk})

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.valid_link:
            context['valid_link'] = True
        else:
            context.update({
                'form': None,
                'valid_link': False,
            })
        return context


class PasswordRecover(auth_views.PasswordResetView):
    """
    密码找回页面，填写邮箱
    """
    title = '密码找回'
    form_class = PasswordResetForm
    # from_email = settings.DEFAULT_FROM_EMAIL
    email_template_name = 'account/password/reset_email.html'
    html_email_template_name = 'mail/general.html'
    success_url = reverse_lazy('portal:account_password_recover_done')
    template_name = 'account/password/recover.html'
    subject_template_name = 'account/password/reset_subject.txt'

    def form_valid(self, form):
        self.extra_email_context = {
            'host': self.request.META['HTTP_HOST'],  # fixme
            'date': timezone.now().strftime('%Y-%m-%d')}
        # messages.add_message(self.request, messages.SUCCESS, '找回密码成功')
        return super().form_valid(form)


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    """
    用户通过正确的链接进入密码重置页面
    """
    form_class = SetPasswordForm
    template_name = 'account/password/reset_confirm.html'
    success_url = reverse_lazy('portal:account_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # user = form.user
        # user.password_updated_at = timezone.now()
        # user.need_to_change_password = False
        # user.save()
        # messages.add_message(self.request, messages.SUCCESS, '你的密码已修改成功，请登录。')
        return response
