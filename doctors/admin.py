from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(TranslatableAdmin):
    list_display = ('full_name', 'position', 'email', 'phone', 'is_active', 'order', 'all_languages_column')
    list_filter = ('is_active', 'translations__position') # position tarjima qilingan maydon
    search_fields = ('translations__full_name', 'translations__position', 'translations__bio', 'email', 'phone')
    list_editable = ('order', 'is_active') # Ro'yxatdan turib o'zgartirish mumkin

    fieldsets = (
        (None, {
            'fields': ('full_name', 'position', 'photo', 'email', 'phone', 'experience_years', 'is_active', 'order')
        }),
        ('Biography (All Languages)', {
            'fields': ('bio',)
        }),
    )