from django.contrib import admin
from parler.admin import TranslatableAdmin # Ko'p tilli modellar uchun
from django_ckeditor_5.fields import CKEditor5Field
from .models import NewsCategory, News

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__', 'all_languages_column') # Kategoriya nomini va mavjud tillarni ko'rsatadi
    # `all_languages_column` parler tomonidan taqdim etiladi
    
    # Slug avtomatik to'ldirilishi uchun (agar TranslatedFields ichida bo'lsa)
    # Parler odatda o'zi buni yaxshi boshqaradi, lekin kerak bo'lsa:
    # def get_prepopulated_fields(self, request, obj=None):
    #     # Joriy til uchun slugni avtomatik to'ldirish
    #     return {'slug': ('name',)} # Bu yerda 'name' translated field bo'lishi kerak
    # Bu qismni parler o'zi hal qiladi, agar TranslatedFields to'g'ri sozlanagan bo'lsa

@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ('title', 'category', 'published_date', 'is_published', 'all_languages_column')
    list_filter = ('is_published', 'category', 'published_date')
    search_fields = ('translations__title', 'translations__content') # Tarjima qilingan maydonlar bo'yicha qidiruv
    # `translations__` prefiksi bilan tarjima qilingan maydonlarga murojaat qilinadi

    # Sarlavhadan slugni avtomatik to'ldirish (agar TranslatedFields ichida bo'lsa)
    # def get_prepopulated_fields(self, request, obj=None):
    # return {'slug': ('title',)} # Bu ham parler tomonidan boshqariladi
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'image', 'is_published') # 'published_date' olib tashlandi
        }),
        ('Content (All Languages)', { # Bu sarlavha admin panelida ko'rinadi
            'fields': ('content', 'keywords') # Bu yerda 'content' va 'keywords' TranslatableFields
        }),
    )
    readonly_fields = ('published_date',) # published_date faqat readonly_fields ichida
    # CKEditor5Field uchun maxsus sozlash shart emas
    # `content` maydoni avtomatik ravishda CKEditor bilan ko'rsatiladi, chunki modelda RichTextField ishlatilgan.