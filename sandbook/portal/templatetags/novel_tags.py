from django import template
from django.db.models import QuerySet, Count, Sum

from base.models import Chapter
from general.utils.datetime import humanize_datetime_simple

register = template.Library()


@register.filter
def novel_status_color(novel):
    status_mappings = {
        1: 'warning',  # 未审核
        2: 'success',  # 连载中
        3: 'secondary',  # 已完结
        4: 'danger',  # 已屏蔽
    }
    return status_mappings.get(novel.status) or 'info'


@register.filter
def next_chapter(chapter):
    volume = chapter.volume
    novel = volume.novel
    # 本卷是否有更新的章节
    newer_chapters = chapter.volume.chapter_set.filter(id__gt=chapter.id).order_by('id')
    if newer_chapters:
        return newer_chapters.first()

    # 是否有下一卷
    newer_volumes = novel.volume_set.filter(id__gt=volume.id)
    if newer_volumes:
        newer_volume = newer_volumes.first()
        if newer_volume:
            return newer_volume.chapter_set.first()
    return


@register.filter
def previous_chapter(chapter):
    volume = chapter.volume
    novel = volume.novel
    # 本卷是否有更老的章节
    older_chapters = chapter.volume.chapter_set.filter(id__lt=chapter.id).order_by('id')
    if older_chapters:
        return older_chapters.last()

    # 是否有前一卷
    older_volumes = novel.volume_set.filter(id__lt=volume.id).order_by('id')
    if older_volumes:
        older_volume = older_volumes.last()
        if older_volume:
            return older_volume.chapter_set.last()
    return


@register.filter
def volume_word_count(volume):
    result = volume.chapter_set.aggregate(Sum('word_count'))
    return result['word_count__sum']
