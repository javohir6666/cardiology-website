# pages/views.py
from django.views.generic import DetailView
from .models import Page
from parler.views import TranslatableSlugMixin
# from django.utils.translation import gettext_lazy as _
from django.http import Http404


class PageDetailView(TranslatableSlugMixin, DetailView):
    model = Page
    template_name_field = 'template_name' # Modelda shablon nomini saqlaydigan maydon
    context_object_name = 'page'
    # slug_field va slug_url_kwarg TranslatableSlugMixin tomonidan avtomatik aniqlanadi

    def get_queryset(self):
        # Faqat chop etilgan sahifalarni olish
        return super().get_queryset().filter(is_published=True).prefetch_related('translations')

    def get_template_names(self):
        # Agar obyektda (page) maxsus shablon nomi ko'rsatilgan bo'lsa, o'shani ishlatamiz.
        # Aks holda, standart 'pages/page_detail.html' ni ishlatamiz.
        if self.object and self.object.template_name:
            return [self.object.template_name]
        return ["pages/page_detail.html"] # Standart shablon

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # `object` allaqachon TranslatableSlugMixin tomonidan to'g'ri tilda topilgan bo'ladi
        context['page_title'] = self.object.safe_translation_getter('title', any_language=True)
        return context