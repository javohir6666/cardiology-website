from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field

class NewsCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Category Name"), max_length=200),
        slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True, help_text=_("URL uchun. Agar bo'sh qoldirilsa, nomidan avtomatik generatsiya qilinadi."))
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or _("Nomsiz Kategoriya")

    def save(self, *args, **kwargs):
        # Agar slug bo'sh bo'lsa va nom mavjud bo'lsa, uni avtomatik generatsiya qilish
        if not self.slug and self.name:
            self.slug = slugify(self.name) # Yoki har bir til uchun alohida slug yaratish logikasi
        super().save(*args, **kwargs)

    # Agar har bir til uchun alohida slug kerak bo'lsa, parler bilan quyidagicha qilish mumkin:
    # 1. Slugni TranslatedFields ichiga olib o'tish.
    # 2. Har bir tarjimani saqlashdan oldin slugni generatsiya qilish.
    # Biz hozirda slugni tarjima qilinadigan qildik.

class News(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("Title"), max_length=255),
        slug = models.SlugField(_("Slug"), max_length=270, unique=True, blank=True, help_text=_("URL uchun. Agar bo'sh qoldirilsa, sarlavhadan avtomatik generatsiya qilinadi.")),
        content = CKEditor5Field(_("Content"), config_name='default'),
        keywords = models.CharField(_("Keywords"), max_length=255, blank=True, null=True, help_text=_("Vergul bilan ajratilgan kalit so'zlar"))
    )
    category = models.ForeignKey(NewsCategory, related_name='news_items', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))
    image = models.ImageField(_("Image"), upload_to='news_images/%Y/%m/%d/')
    published_date = models.DateTimeField(_("Published Date"), auto_now_add=True) # Yoki default=timezone.now
    is_published = models.BooleanField(_("Is Published"), default=True)
    views_count = models.PositiveIntegerField(_("Views Count"), default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-published_date']

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or _("Nomsiz Yangilik")

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self): # Saytda yangilikka link olish uchun
        # Bu yerda URL nomini to'g'ri ko'rsatish kerak (urls.py da aniqlanadi)
        # Masalan: return reverse('news:news_detail', kwargs={'slug': self.slug})
        # Ko'p tilli URLlar uchun parler o'zi to'g'rilaydi agar URL i18n_patterns ichida bo'lsa
        # Yoki har bir til uchun alohida slug bilan:
        # return reverse('news:news_detail', kwargs={'slug': self.safe_translation_getter('slug')})
        try:
            # Eng yaxshi yo'li: current language slug orqali
            return reverse('news:news_detail', kwargs={'slug': self.safe_translation_getter('slug', language_code=self.get_current_language()) or self.slug})
        except Exception:
            return "/"