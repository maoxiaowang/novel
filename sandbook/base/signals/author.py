from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from base.models import User
from base.models.account import Notification
from base.models.author import AuthorApplication


@receiver(post_save, sender=AuthorApplication)
def on_application_changed(sender, instance, **kwargs):
    if kwargs.get('created'):
        # 给管理员发送通知
        ...
    else:
        if instance.status == instance.STATUS_AGREE:
            # 审核通过，给用户发送通知
            approver = instance.approver
            approver.is_author = True
            approver.save()

            # Notification
            Notification.objects.create(
                title='恭喜你', content='你提交的成为作家的请求已经通过，可以前往作品管理处发布作品。',
                sender=instance.approver, receiver=instance.applier, level=Notification.LEVEL_SUCCESS
            )
        elif instance.status == instance.STATUS_REJECT:
            # 审核拒绝
            Notification.objects.create(
                title='很遗憾', content='你提交的成为作家的请求未通过，可以前往帮助中心寻求帮助。',
                sender=instance.approver, receiver=instance.applier, level=Notification.LEVEL_ERROR
            )
