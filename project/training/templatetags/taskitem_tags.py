from datetime import datetime
from django import template

register = template.Library()


@register.inclusion_tag('training/taskitem/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}


@register.filter
def date_format(str_datetime):
    val = datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S.%f')
    return val.strftime('%Y.%m.%d [%H:%M]')
