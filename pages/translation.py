from modeltranslation.translator import register, TranslationOptions
from .models import Page, MenuItem

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'content', 'meta_keywords', 'meta_description',)

@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('title',)
