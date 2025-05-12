from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Page, MenuItem

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content_uz': CKEditor5Widget(),
            'content_ru': CKEditor5Widget(),
            'content_en': CKEditor5Widget(),
        }

@admin.register(Page)
class PageAdmin(TranslationAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'meta_keywords', 'meta_description', 'template_name', 'is_published')
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin, TranslationAdmin):
    list_display = ('tree_actions', 'indented_title', 'location', 'is_active')
    search_fields = ('title',)
    list_filter = ('location', 'is_active')
    prepopulated_fields = {}