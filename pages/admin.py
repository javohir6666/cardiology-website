from django.contrib import admin
from parler.admin import TranslatableAdmin
from mptt.admin import DraggableMPTTAdmin # MPTT modellari uchun
from .models import Page, MenuItem
from django_ckeditor_5.fields import CKEditor5Field

@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ('title', 'slug', 'template_name', 'is_published', 'all_languages_column')
    list_filter = ('is_published', 'template_name')
    search_fields = ('translations__title', 'translations__slug', 'translations__content')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'template_name', 'is_published')
        }),
        ('Content (All Languages)', {
            'fields': ('content',)
        }),
        ('SEO (All Languages)', {
            'classes': ('collapse',), # Bu bo'lim yopiq turadi, bosganda ochiladi
            'fields': ('meta_keywords', 'meta_description')
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(TranslatableAdmin, DraggableMPTTAdmin): # Ikkalasidan ham vorislik olamiz
    list_display = ('tree_actions', 'indented_title', 'link_page', 'link_url', 'location', 'order', 'is_active', 'all_languages_column')
    list_display_links = ('indented_title',) # Qaysi ustun orqali tahrirlashga o'tish
    list_filter = ('location', 'is_active', 'parent')
    search_fields = ('translations__title', 'link_url')
    list_editable = ('order', 'is_active')

    # DraggableMPTTAdmin sozlamalari
    mptt_level_indent = 20 # Har bir ichki daraja uchun qancha joy tashlash (pikselda)
    
    # TranslatableAdmin va MPTTAdmin birgalikda ishlashi uchun ba'zan formani aniq ko'rsatish kerak bo'lishi mumkin
    # lekin odatda avtomatik ishlaydi.

    # `title` (sarlavha) tarjima qilinadigan maydon bo'lgani uchun `indented_title` yaxshi ishlaydi.
    # Agar muammo bo'lsa, maxsus metod yozib, uni `list_display` ga qo'shish mumkin.