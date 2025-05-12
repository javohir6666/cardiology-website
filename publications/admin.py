from django.contrib import admin
from parler.admin import TranslatableAdmin
from django_ckeditor_5.fields import CKEditor5Field
from .models import PublicationCategory, Publication

@admin.register(PublicationCategory)
class PublicationCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__', 'all_languages_column')
    # def get_prepopulated_fields(self, request, obj=None):
    #     return {'slug': ('name',)}

@admin.register(Publication)
class PublicationAdmin(TranslatableAdmin):
    list_display = ('title', 'category', 'publication_year', 'is_published', 'all_languages_column')
    list_filter = ('is_published', 'category', 'publication_year')
    search_fields = ('translations__title', 'translations__content')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'cover_image', 'file', 'publication_year', 'publisher', 'is_published')
        }),
        ('Content (All Languages)', {
            'fields': ('content',)
        }),
    )
    # CKEditor5Field uchun maxsus sozlash shart emas