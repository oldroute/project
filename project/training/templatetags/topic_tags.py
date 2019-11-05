from django import template

register = template.Library()


@register.inclusion_tag('training/topic/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}
