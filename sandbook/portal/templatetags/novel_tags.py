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
    newer_chapters = Chapter.objects.filter(id__gt=chapter.id).order_by('id')
    if newer_chapters:
        return newer_chapters.first()
    return


@register.filter
def previous_chapter(chapter):
    older_chapters = Chapter.objects.filter(id__lt=chapter.id).order_by('id')
    if older_chapters:
        return older_chapters.last()
    return


@register.filter
def volume_word_count(volume):
    result = volume.chapter_set.aggregate(Sum('word_count'))
    return result['word_count__sum']
