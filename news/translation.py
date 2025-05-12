from modeltranslation.translator import register, TranslationOptions
from .models import News, NewsCategory

@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'content', 'keywords',)
