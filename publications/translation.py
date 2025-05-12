from modeltranslation.translator import register, TranslationOptions
from .models import Publication, PublicationCategory

@register(PublicationCategory)
class PublicationCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

@register(Publication)
class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'short_description', 'content', 'publisher',)
