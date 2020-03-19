from django import template

from general.utils.datetime import humanize_datetime_simple

register = template.Library()


@register.filter(is_safe=True)
def to_label(field, cls=''):
    """
    Passing a field and return it's label with a class
    """
    if not field:
        return ''
    if 'text-' not in cls and field.field.required is False:
        cls += ' text-muted'
    return field.label_tag(attrs={'class': cls})


@register.filter(is_safe=True)
def render_datetime(dt, show_direction=True):
    return humanize_datetime_simple(dt, show_direction=show_direction)
