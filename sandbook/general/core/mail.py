from django.conf import settings
from django.core import mail


def send_mail(subject, message, recipient_list, from_email=None, bcc=None, cc=None,
              content_type='html', **kwargs):
    assert content_type in ('html', 'plain')

    # 防止被认为垃圾邮件（163邮箱）
    default_cc = [settings.DEFAULT_FROM_EMAIL]
    if cc:
        assert isinstance(cc, list)
        default_cc.extend(cc)
    email = mail.EmailMessage(
        subject,
        message,
        from_email=from_email,
        to=recipient_list,
        cc=default_cc,
        bcc=bcc,
        **kwargs
    )
    setattr(email, 'content_subtype', content_type)
    email.send()
