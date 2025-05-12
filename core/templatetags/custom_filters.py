from django import template
from django.urls import NoReverseMatch
import os

register = template.Library()

@register.filter
def filename(value):
    if hasattr(value, 'name'):
        return os.path.basename(value.name)
    return ''

@register.simple_tag(takes_context=True)
def active_link(context, link_url_or_name, current_path, return_value='active', check_starts_with=False):
    try:
        url_to_check = link_url_or_name
    except NoReverseMatch:
        url_to_check = link_url_or_name
    if check_starts_with:
        if current_path.startswith(str(url_to_check)):
            return return_value
    else:
        if str(url_to_check) == str(current_path):
            return return_value
    return ''

@register.filter
def split_by(value, delimiter=','):
    """Stringni delimiter bo'yicha bo'lib, har bir elementni strip qiladi."""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter)]

@register.filter
def get_item(dictionary, key):
    """Template filter: dictionary[key]"""
    return dictionary.get(key)