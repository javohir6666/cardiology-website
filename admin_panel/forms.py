from django import forms
from news.models import News, NewsCategory
from pages.models import Page
from publications.models import Publication, PublicationCategory
from doctors.models import Doctor
from core.models import GalleryImage
from parler.forms import TranslatableModelForm
from django_ckeditor_5.widgets import CKEditor5Widget

class NewsForm(TranslatableModelForm):
    class Meta:
        model = News
        fields = [
            'title', 'slug', 'content', 'keywords',
            'category', 'image', 'is_published',
        ]
        widgets = {
            'content': CKEditor5Widget(config_name='default'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Parler TranslatedFields uchun CKEditor5Widget ni aniq o'rnatish
        if 'content' in self.fields:
            self.fields['content'].widget = CKEditor5Widget(config_name='default')
        for field_name, field in self.fields.items():
            if field_name == 'content':
                continue  # CKEditor5Widget allaqachon o'rnatildi
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'

class NewsCategoryForm(TranslatableModelForm):
    class Meta:
        model = NewsCategory
        fields = ['name', 'slug']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PageForm(TranslatableModelForm):
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'content', 'meta_keywords', 'meta_description',
            'template_name', 'is_published',
        ]
        widgets = {
            'content': CKEditor5Widget(config_name='default'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'content' in self.fields:
            self.fields['content'].widget = CKEditor5Widget(config_name='default')
        for field_name, field in self.fields.items():
            if field_name == 'content':
                continue
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'

class PublicationForm(TranslatableModelForm):
    class Meta:
        model = Publication
        fields = [
            'title', 'slug', 'short_description', 'content', 'authors',
            'category', 'cover_image', 'file', 'publication_year', 'publisher', 'is_published',
        ]
        widgets = {
            'short_description': CKEditor5Widget(config_name='default'),
            'content': CKEditor5Widget(config_name='default'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'content' in self.fields:
            self.fields['content'].widget = CKEditor5Widget(config_name='default')
        if 'short_description' in self.fields:
            self.fields['short_description'].widget = CKEditor5Widget(config_name='default')
        for field_name, field in self.fields.items():
            if field_name in ['content', 'short_description']:
                continue
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['cover_image', 'file']:
                field.widget.attrs['class'] = 'form-control-file'
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'

class PublicationCategoryForm(TranslatableModelForm):
    class Meta:
        model = PublicationCategory
        fields = ['name', 'slug']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DoctorForm(TranslatableModelForm):
    class Meta:
        model = Doctor
        fields = [
            'full_name', 'position', 'bio',
            'photo', 'email', 'phone', 'experience_years',
            'is_active', 'order',
        ]
        widgets = {
            'bio': CKEditor5Widget(config_name='default'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bio' in self.fields:
            self.fields['bio'].widget = CKEditor5Widget(config_name='default')
        for field_name, field in self.fields.items():
            if field_name == 'bio':
                continue
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'photo':
                field.widget.attrs['class'] = 'form-control-file'
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'title']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'
