# core/context_processors.py
from pages.models import MenuItem # MenuItem modelini pages ilovasidan import qilamiz
from django import template
from django.urls import reverse, NoReverseMatch
import os
register = template.Library()

def main_menu_items(request):
    # Faqat aktiv va 'main_menu' joylashuvidagi menyu bandlarini olamiz
    # MPTT ning get_cached_trees() metodi so'rovlar sonini kamaytiradi
    menu_items = MenuItem.objects.filter(is_active=True, location='main_menu').prefetch_related('translations')
    return {'menu_items_main': menu_items}

def footer_menu_items(request):
    menu_items = MenuItem.objects.filter(is_active=True, location='footer_menu').prefetch_related('translations')
    return {'menu_items_footer': menu_items}

@register.filter
def filename(value):
    if hasattr(value, 'name'):
        return os.path.basename(value.name)
    return ''


@register.simple_tag(takes_context=True) # takes_context=True qilib o'zgartirdik
def active_link(context, link_url_or_name, current_path, return_value='active', check_starts_with=False):
    """
    Checks if the given link (URL or named URL) matches or starts with the current path.
    If 'check_starts_with' is True, it checks if current_path starts with the link.
    Useful for parent menu items in dropdowns.
    """
    try:
        # Agar named URL bo'lsa, uni haqiqiy URLga aylantiramiz
        # Bu qism murakkablashishi mumkin, agar link_url_or_name Page modelidan kelsa
        # va u allaqachon to'liq URL bo'lsa. MenuItem.get_link() to'g'ri URL qaytarishi kerak.
        # Hozircha, link_url_or_name to'g'ridan-to'g'ri URL deb qabul qilamiz.
        url_to_check = link_url_or_name
    except NoReverseMatch:
        url_to_check = link_url_or_name # Agar oddiy URL bo'lsa

    # Joriy til prefiksini hisobga olish (agar URLlar i18n_patterns ichida bo'lsa)
    # Misol uchun, agar current_path /uz/page/slug/ bo'lsa,
    # va url_to_check /page/slug/ bo'lsa, ularni solishtirish kerak.
    # Bu qismni soddalashtiramiz, MenuItem.get_link() joriy til prefiksi bilan URL qaytaradi deb hisoblaymiz.

    if check_starts_with:
        if current_path.startswith(str(url_to_check)):
            return return_value
    else:
        if str(url_to_check) == str(current_path):
            return return_value
    return ''

