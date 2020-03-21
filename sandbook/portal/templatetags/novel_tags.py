from django import template

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
