import os

from django.contrib.auth import models as auth_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.constants.account import MANAGEMENT_GROUP_IDS, WORK_MANAGER_GROUP_ID, USER_MANAGER_GROUP_ID


class Group(auth_model.Group):
    """
    用户组

    作者组（所有作者）
    小说管理组（小说审核，屏蔽，解封，删除）
    用户管理组（用户行为管理，封号，禁言，删除评论，发送站内信）
    """
    class Meta:
        proxy = True


created_at = models.DateTimeField('创建时间', default=timezone.now)
created_at.contribute_to_class(auth_model.Group, 'created_at')
description = models.CharField('描述', max_length=100)
description.contribute_to_class(auth_model.Group, 'description')


class Permission(auth_model.Permission):
    """
    权限
    """
    class Meta:
        proxy = True


def avatar_path(instance, filename):
    return os.path.join('users', str(instance.id), 'avatars', filename)


class User(AbstractUser):
    """
    用户
    """
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        '用户名',
        max_length=32,
        unique=True,
        help_text=_(
            'Required. 32 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    groups = models.ManyToManyField(
        'base.Group')
    user_permissions = models.ManyToManyField(
        'base.Permission')
    teams = models.ManyToManyField('base.Team')
    nickname = models.CharField(
        '昵称',
        max_length=150,
        validators=[UnicodeUsernameValidator],
        blank=True,
        help_text=_('Nick name is only used to display.')
    )
    avatar = models.ImageField(
        '头像', storage=FileSystemStorage(),
        default='default/avatars/user.jpg',
        upload_to=avatar_path, blank=True
    )
    description = models.CharField(
        '描述', max_length=100, blank=True
    )
    is_locked = models.BooleanField(default=False)  # 锁定
    is_muted = models.BooleanField(default=False)  # 禁言
    is_author = models.BooleanField(default=False)  # True时才会有AuthorInfo
    is_robot = models.BooleanField(default=False)  # True时无法登陆，系统机器人

    class Meta:
        db_table = 'auth_user'
        default_permissions = ()
        permissions = (
            # ('create_user', '创建用户'),  暂不需要，为管理员权限
            # ('view_user', '查看用户'),
            # ('delete_user', '删除用户'),
            # ('change_user', '修改用户'),
            ('lock_user', '锁定用户'),
        )

    @property
    def is_manager(self):
        return self.groups.filter(id__in=MANAGEMENT_GROUP_IDS).exists()

    @property
    def is_work_manager(self):
        return self.groups.filter(id=WORK_MANAGER_GROUP_ID).exists()

    @property
    def is_user_manager(self):
        return self.groups.filter(id=USER_MANAGER_GROUP_ID).exists()

    def get_display_name(self):
        return self.nickname or self.username


class UserInfo(models.Model):
    """
    用户详细信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    exp = models.PositiveIntegerField('经验值', default=0)

    class Meta:
        db_table = 'auth_user_info'
        default_permissions = ()


class AuthorInfo(models.Model):
    """
    作者详细信息
    """
    LEVEL_CHOICES = (
        (0, '普通'),
        (1, '青铜'),
        (2, '白银'),
        (3, '黄金'),
        (4, '钻石'),
        (5, '铂金')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    pen_name = models.CharField('笔名', max_length=32, unique=True, null=True, default=None,
                                validators=[UnicodeUsernameValidator])
    level = models.PositiveSmallIntegerField('等级', choices=LEVEL_CHOICES, default=0)
    date_joined = models.DateTimeField('成为作者的日期', default=timezone.now)

    class Meta:
        db_table = 'auth_author_info'
        default_permissions = ()


class Team(models.Model):
    """
    小组
    """
    name = models.CharField('名称', max_length=32)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    description = models.CharField('描述', max_length=255)

    class Meta:
        db_table = 'auth_team'
        default_permissions = ()


class Notification(models.Model):
    """
    通知
    """
    LEVEL_NORMAL = 0
    LEVEL_SUCCESS = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3
    LEVEL_CHOICES = (
        (LEVEL_NORMAL, '普通'),
        (LEVEL_SUCCESS, '成功'),
        (LEVEL_WARNING, '警告'),
        (LEVEL_ERROR, '错误'),
    )
    title = models.CharField('标题', max_length=32)
    content = models.CharField('内容', max_length=1024)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='接受者')
    level = models.SmallIntegerField('等级', default=0, choices=LEVEL_CHOICES)
    read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'base_notifications'
        default_permissions = ()


class Following(models.Model):
    """
    关注
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='被关注者')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', verbose_name='关注者')
    created_at = models.DateTimeField('关注于', auto_now_add=True)

    class Meta:
        db_table = 'base_user_following'
        default_permissions = ()


class Activity(models.Model):
    """
    （圈子）动态
    """
    TYPE_CHOICES = (
        (1, '魔法日记'),  # 用户个人（及关注的人）发表的动态
        (2, '成长之路'),  # 用户相关记录，如升级，连续更新，连续鸽，获得称号等
        (3, '其他')  # 未定
    )
    type = models.PositiveSmallIntegerField('类型')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField('标题', max_length=64)
    content = models.CharField('内容', max_length=1024)
    created_at = models.DateTimeField('发布于', auto_now_add=True)

    class Meta:
        db_table = 'base_user_activity'
        default_permissions = ()


class ActivityLikes(models.Model):
    """
    动态点赞
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='动态', related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField('点赞于', auto_now_add=True)

    class Meta:
        db_table = 'base_user_activity_likes'
        default_permissions = ()


class ActivityComment(models.Model):
    """
    动态评论
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='动态', related_name='comments')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, verbose_name='用户')
    content = models.CharField('内容', max_length=1024)
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_user_activity_comment'
        default_permissions = ()


class ActivityCommentReply(models.Model):
    """
    动态评论回复
    """
    activity_comment = models.ForeignKey(ActivityComment, on_delete=models.CASCADE, verbose_name='动态评论')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True,
                             related_name='ac_reply_user', verbose_name='回复用户')
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_user_activity_comment_reply'
        default_permissions = ()

