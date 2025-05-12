from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field

class NewsCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True, help_text=_("URL uchun. Agar bo'sh qoldirilsa, nomidan avtomatik generatsiya qilinadi."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")

    def __str__(self):
        return self.name or _("Nomsiz Kategoriya")

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class News(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=270, unique=True, blank=True, help_text=_("URL uchun. Agar bo'sh qoldirilsa, sarlavhadan avtomatik generatsiya qilinadi."))
    content = CKEditor5Field(_("Content"), config_name='default')
    keywords = models.CharField(_("Keywords"), max_length=255, blank=True, null=True, help_text=_("Vergul bilan ajratilgan kalit so'zlar"))
    category = models.ForeignKey(NewsCategory, related_name='news_items', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))
    image = models.ImageField(_("Image"), upload_to='news_images/%Y/%m/%d/')
    published_date = models.DateTimeField(_("Published Date"), auto_now_add=True)
    is_published = models.BooleanField(_("Is Published"), default=True)
    views_count = models.PositiveIntegerField(_("Views Count"), default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-published_date']

    def __str__(self):
        return self.title or _("Nomsiz Yangilik")

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('news:news_detail', kwargs={'slug': self.slug})
        except Exception:
            return "/"