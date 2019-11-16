from datetime import datetime
from django import template

register = template.Library()


@register.filter
def date_format(str_datetime):
    if str_datetime:
        val = datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S.%f')
        return val.strftime('%Y.%m.%d: %H:%M')
    else:
        return '-'


@register.inclusion_tag('training/parts/breadcrumbs.html', takes_context=True)
def show_breadcrumbs(context):
    return context


@register.inclusion_tag('training/parts/sidebar.html')
def show_sidebar(course):
    return {'data': course.get_cache_data()}
