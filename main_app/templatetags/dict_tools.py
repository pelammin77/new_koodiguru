# Tiedostossa templatetags/dict_tools.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={'class': css})