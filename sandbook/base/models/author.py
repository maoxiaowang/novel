from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class AuthorApplication(models.Model):
    """
    申请成为作者
    """
    STATUS = {
        'unapproved': 0,
        'agreed': 1,
        'rejected': 2
    }
    STATUS_CHOICES = (
        (STATUS['unapproved'], '未审核'),
        (STATUS['agreed'], '通过'),
        (STATUS['rejected'], '拒绝'),
    )
    applier = models.ForeignKey('base.User', on_delete=models.CASCADE, related_name='applier')
    status = models.SmallIntegerField(default=0)
    approver = models.ForeignKey('base.User', on_delete=models.CASCADE, related_name='approver',
                                 null=True, default=None, verbose_name='审批者')
    pen_name = models.CharField('笔名', max_length=32, validators=[UnicodeUsernameValidator])
    self_intro = models.TextField('给编辑的话', max_length=512, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'base_author_application'
        default_permissions = ()
