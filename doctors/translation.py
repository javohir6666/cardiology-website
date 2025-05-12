from modeltranslation.translator import register, TranslationOptions
from .models import Doctor

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'bio',)
