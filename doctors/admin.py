from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Doctor

class DoctorAdminForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'bio_uz': CKEditor5Widget(),
            'bio_ru': CKEditor5Widget(),
            'bio_en': CKEditor5Widget(),
        }

@admin.register(Doctor)
class DoctorAdmin(TranslationAdmin):
    form = DoctorAdminForm
    list_display = ('full_name', 'position', 'is_active', 'order')
    search_fields = ('full_name', 'position')
    list_filter = ('is_active',)
    ordering = ('order', 'full_name')