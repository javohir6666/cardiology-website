from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django_ckeditor_5.fields import CKEditor5Field
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import PublicationCategory, Publication

class PublicationAdminForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'
        widgets = {
            'content_uz': CKEditor5Widget(),
            'content_ru': CKEditor5Widget(),
            'content_en': CKEditor5Widget(),
            'short_description_uz': CKEditor5Widget(),
            'short_description_ru': CKEditor5Widget(),
            'short_description_en': CKEditor5Widget(),
        }

@admin.register(PublicationCategory)
class PublicationCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Publication)
class PublicationAdmin(TranslationAdmin):
    form = PublicationAdminForm
    list_display = ('title', 'category', 'publication_year', 'is_published')
    list_filter = ('is_published', 'category', 'publication_year')
    search_fields = ('title', 'content')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'cover_image', 'file', 'publication_year', 'publisher', 'is_published')
        }),
        ('Content', {
            'fields': ('content', 'short_description')
        }),
    )