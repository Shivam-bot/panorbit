from django import template

register = template.Library()


@register.filter
def match_select_value(obj, d):
    print(obj, d,"vbnkl;lkmn")
    show = ''
    if obj == d:
        show = 'selected'
    return show