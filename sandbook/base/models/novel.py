import os
import re
import time

from django.core.files.storage import FileSystemStorage
from django.db import models

from base.constants.novel import (
    DEFAULT_COVER, NOVEL_STATUS_UNAPPROVED, NOVEL_STATUS_ACTIVE, NOVEL_STATUS_FINISHED,
    NOVEL_STATUS_BLOCKED
)
from django.core.cache import cache

from general.utils.text import get_filename_extension, calc_word_count


class CategoryMixin:

    @property
    def novel_count_key(self):
        raise NotImplementedError

    def novel_count(self):
        return cache.get(self.novel_count_key)


class Category(CategoryMixin, models.Model):
    """
    一级分类
    """
    name = models.CharField('名称', max_length=32)
    description = models.CharField('描述', max_length=255)

    class Meta:
        db_table = 'base_novel_category'

    def __str__(self):
        return self.name

    @property
    def novel_count_key(self):
        return 'sc_%d_count' % self.id


class SubCategory(CategoryMixin, models.Model):
    """
    二级分类
    """
    name = models.CharField('名称', max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='一级分类')
    description = models.CharField('描述', max_length=255)

    class Meta:
        db_table = 'base_novel_sub_category'
        default_permissions = ()

    def __str__(self):
        return self.name

    @property
    def novel_count_key(self):
        return 'c_%d_count' % self.id

    def incr_novel_count(self, count: int):
        """
        count 可以为正负整数
        """
        cache.incr(self.novel_count_key, count)


def cover_path(instance, filename):
    new_name = '%s.%s' % (str(int(time.time())), get_filename_extension(filename))
    return os.path.join('novel', 'cover', str(instance.author_id), new_name)


class Novel(models.Model):
    """
    小说
    """
    STATUS = {
        'unapproved': NOVEL_STATUS_UNAPPROVED,
        'active': NOVEL_STATUS_ACTIVE,
        'finished': NOVEL_STATUS_FINISHED,
        'blocked': NOVEL_STATUS_BLOCKED,
    }
    STATUS_CHOICES = (
        (STATUS['unapproved'], '未审核'),
        (STATUS['active'], '连载中'),
        (STATUS['finished'], '已完结'),
        (STATUS['blocked'], '已屏蔽')
    )
    name = models.CharField('书名', unique=True, max_length=64)  # TODO: 书名验证
    author = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, verbose_name='作者')
    intro = models.TextField('简介', max_length=1024)
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=NOVEL_STATUS_UNAPPROVED)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='一级分类')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, verbose_name='二级分类')
    cover = models.ImageField(
        '封面', storage=FileSystemStorage(), default=DEFAULT_COVER,
        upload_to=cover_path, blank=True
    )
    word_count = models.PositiveIntegerField('字数', default=0)
    created_at = models.DateTimeField('创建于', auto_now_add=True)
    updated_at = models.DateTimeField('更新于', auto_now=True)

    class Meta:
        db_table = 'base_novel'
        ordering = ('-id',)
        default_permissions = ()
        permissions = (
            ('view_novel', '查看小说'),
            ('create_novel', '创建小说'),
            ('change_novel', '更改小说'),
            ('delete_novel', '删除小说'),
            ('finish_novel', '完结小说'),
            ('block_novel', '屏蔽小说'),
            ('verify_novel', '审核小说')
        )


class NovelComment(models.Model):
    """
    书评
    """
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='小说')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, verbose_name='用户')
    title = models.CharField('标题', max_length=32, blank=True)  # 标题可选
    content = models.CharField('内容', max_length=4096)
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_novel_comment'
        default_permissions = ()


class NovelCommentReply(models.Model):
    """
    书评回复
    """
    novel_comment = models.ForeignKey(NovelComment, on_delete=models.CASCADE, verbose_name='书评')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True,
                             related_name='nc_reply_user', verbose_name='回复用户')
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_novel_comment_reply'
        default_permissions = ()


class Volume(models.Model):
    """
    卷
    """
    name = models.CharField('卷名', max_length=32, default='正文卷')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='小说')
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_novel_volume'
        default_permissions = ()


class Chapter(models.Model):
    """
    章节
    """
    STATUS = {
        'saved': 0,
        'submitted': 1,
        'blocked': 2,
        'approved': 3  # 暂不用
    }
    STATUS_CHOICES = (
        (STATUS['saved'], '已保存'),
        (STATUS['submitted'], '已提交'),
        (STATUS['blocked'], '已屏蔽'),
        (STATUS['approved'], '已审核')
    )

    title = models.CharField('标题', max_length=32, blank=True, default='新章节')  # TODO: 章节名验证
    content = models.TextField('内容', max_length=65535, blank=True)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, verbose_name='卷')
    word_count = models.PositiveIntegerField('字数', default=0)
    is_free = models.BooleanField('免费', default=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=STATUS['saved'])
    created_at = models.DateTimeField('创建于', auto_now_add=True)
    updated_at = models.DateTimeField('更新于', auto_now=True)

    class Meta:
        db_table = 'base_novel_chapter'
        default_permissions = ()


# class ChapterUpdated(models.Model):
#     ...


class Paragraph(models.Model):
    """
    段落
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='章节')
    content = models.TextField('内容', max_length=65535)  # TODO: 段落字数限制
    serial = models.PositiveIntegerField('序号', default=1)

    class Meta:
        db_table = 'base_novel_paragraph'
        default_permissions = ()
        unique_together = (('chapter', 'serial'),)

    @property
    def word_count(self):
        return calc_word_count(self.content)


class ParagraphComment(models.Model):
    """
    段评
    """
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, verbose_name='段落')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, verbose_name='用户')
    content = models.CharField('内容', max_length=1024)
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_novel_paragraph_comment'
        default_permissions = ()


class ParagraphCommentReply(models.Model):
    """
    段评回复
    """
    paragraph_comment = models.ForeignKey(ParagraphComment, on_delete=models.CASCADE, verbose_name='段评')
    user = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True,
                             related_name='pc_reply_user', verbose_name='回复用户')
    created_at = models.DateTimeField('创建于', auto_now_add=True)

    class Meta:
        db_table = 'base_novel_paragraph_comment_reply'
        default_permissions = ()
