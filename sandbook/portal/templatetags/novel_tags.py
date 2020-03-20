from django import template

from general.utils.datetime import humanize_datetime_simple

register = template.Library()


@register.filter
def novel_status_color(novel):
    status_mappings = {
        0: 'warning',  # 未审核
        1: 'success',  # 连载中
        2: 'secondary',  # 已完结
        3: 'danger',  # 已屏蔽
    }
    return status_mappings.get(novel.status) or 'info'
