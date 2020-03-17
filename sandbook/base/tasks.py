from celery import shared_task

from general.core.mail import send_mail


@shared_task
def async_send_email(subject, message, recipient_list, from_email=None, bcc=None, cc=None,
                     content_type='html', **kwargs):
    send_mail(
        subject, message, recipient_list, from_email=from_email, bcc=bcc, cc=cc,
        content_type=content_type, **kwargs
    )
