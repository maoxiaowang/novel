from celery import shared_task
from django.conf import settings
from django.template import loader
from django.utils import timezone
from django.utils.safestring import mark_safe

from general.core.mail import send_mail
from general.task import CommonTask


@shared_task(base=CommonTask)
def send_user_creating_email(recipient_list, username, active_url):
    send_mail(
        '账号注册成功',
        loader.render_to_string(
            'mail/general.html',
            {
                'subject': '欢迎加入SandBook - 沙之书',
                'content': mark_safe(
                    '<p>亲爱的%(username)s: </p>'
                    '<p>欢迎加入SandBook - 沙之书。</p>'
                    '<p>点击下方链接激活你的账户：</p>'
                    '<p><a href="%(active_url)s">%(active_url)s</a></p>' %
                    {'username': username, 'active_url': active_url}
                ),
                'date': timezone.now().strftime('%Y-%m-%d')
            }
        ),
        recipient_list,
    )
