from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field

class PublicationCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Publication Category")
        verbose_name_plural = _("Publication Categories")

    def __str__(self):
        return self.name or _("Nomsiz Kategoriya")

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Publication(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=320, unique=True, blank=True)
    short_description = CKEditor5Field(_("Short Description/Abstract"), blank=True, null=True)
    content = CKEditor5Field(_("Content"), config_name='default')
    authors = models.CharField(_("Authors"), max_length=500, help_text=_("Vergul bilan ajratilgan mualliflar ro'yxati"))
    category = models.ForeignKey(PublicationCategory, related_name='publications', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))
    cover_image = models.ImageField(_("Cover Image"), upload_to='publications_covers/%Y/%m/', blank=True, null=True)
    file = models.FileField(_("File"), upload_to='publications_files/%Y/%m/')
    publication_year = models.PositiveIntegerField(_("Publication Year"), blank=True, null=True)
    publisher = models.CharField(_("Publisher"), max_length=200, blank=True, null=True)
    is_published = models.BooleanField(_("Is Published"), default=True)
    downloads_count = models.PositiveIntegerField(_("Downloads Count"), default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")
        ordering = ['-publication_year', 'title']

    def __str__(self):
        return self.title or _("Nomsiz Nashr")

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)