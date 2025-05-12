# news/admin.py

from django.contrib import admin
from django.conf import settings # settings.LANGUAGE_CODE ni olish uchun
from django.utils.text import slugify
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget # Agar ishlatayotgan bo'lsangiz
from modeltranslation.admin import TranslationAdmin
from .models import News, NewsCategory

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content_uz': CKEditor5Widget(),
            'content_ru': CKEditor5Widget(),
            'content_en': CKEditor5Widget(),
        }

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    form = NewsAdminForm
    list_display = ('title', 'slug', 'created_at', 'is_published')
    list_filter = ('is_published', 'category', 'published_date')
    search_fields = ('title', 'content')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'image', 'slug', 'is_published', 'published_date')
        }),
        ('Content', {
            'fields': ('content', 'keywords')
        }),
    )