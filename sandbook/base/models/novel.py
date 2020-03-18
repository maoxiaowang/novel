from django.db import models


class Category(models.Model):
    """
    一级分类
    """
    name = models.CharField('名称', max_length=32)

    class Meta:
        db_table = 'base_novel_category'


class SubCategory(models.Model):
    """
    二级分类
    """
    name = models.CharField('名称', max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='一级分类')

    class Meta:
        db_table = 'base_novel_sub_category'
        default_permissions = ()


class Novel(models.Model):
    """
    小说
    """
    STATUS_CHOICES = (
        (0, '未审核'),
        (1, '连载中'),
        (2, '已完结'),
        (3, '已屏蔽')
    )
    name = models.CharField('书名', unique=True, max_length=64)  # TODO: 书名验证
    author = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, verbose_name='作者')
    intro = models.TextField('简介', max_length=1024)
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    type_level_two = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    word_count = models.PositiveIntegerField('字数', default=0)
    created_at = models.DateTimeField('创建于', auto_now_add=True)
    updated_at = models.DateTimeField('更新于', auto_now=True)

    class Meta:
        db_table = 'base_novel'
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


class Chapter(models.Model):
    """
    章节
    """
    title = models.CharField('标题', max_length=32)  # TODO: 章节名验证
    content = models.TextField('内容', max_length=65535)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='小说')
    word_count = models.PositiveIntegerField('字数')
    is_free = models.BooleanField('免费', default=True)
    created_at = models.DateTimeField('创建于', auto_now_add=True)
    updated_at = models.DateTimeField('更新于', auto_now=True)

    class Meta:
        db_table = 'base_novel_chapter'
        default_permissions = ()


class Paragraph(models.Model):
    """
    段落
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='章节')
    content = models.TextField('内容', max_length=65535)  # TODO: 段落字数限制
    word_count = models.PositiveIntegerField('字数')
    serial = models.PositiveIntegerField('序号', default=1)

    class Meta:
        db_table = 'base_novel_paragraph'
        default_permissions = ()
        unique_together = (('chapter', 'serial'),)


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