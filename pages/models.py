from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

class Page(models.Model):
    title = models.CharField(_("Page Title"), max_length=255)
    slug = models.SlugField(_("Slug (URL)"), max_length=270, unique=True, help_text=_("Sahifaning URL manzili, masalan 'biz-haqimizda'. Agar bo'sh qoldirilsa, sarlavhadan avtomatik generatsiya qilinadi."))
    content = CKEditor5Field(_("Page Content"), config_name='default')
    meta_keywords = models.CharField(_("Meta Keywords"), max_length=255, blank=True, null=True, help_text=_("SEO uchun kalit so'zlar, vergul bilan ajratilgan."))
    meta_description = models.TextField(_("Meta Description"), blank=True, null=True, help_text=_("SEO uchun sahifa tavsifi."))
    template_name = models.CharField(
        _("Template Name"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Agar maxsus shablon ishlatmoqchi bo'lsangiz, uning nomini kiriting (masalan, 'pages/contact_page.html'). Bo'sh qoldirilsa, standart shablon ishlatiladi.")
    )
    is_published = models.BooleanField(_("Is Published"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title or _("Nomsiz Sahifa")

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('pages:page_detail', kwargs={'slug': self.slug})
        except Exception:
            return "/"


class MenuItem(MPTTModel):
    title = models.CharField(_("Menu Item Title"), max_length=100)
    link_page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Link to Page"), help_text=_("Agar menyu bandi saytdagi sahifaga yo'naltirsa, shu yerdan tanlang."))
    link_url = models.CharField(_("Or Custom URL"), max_length=255, blank=True, help_text=_("Agar menyu bandi tashqi manzilga yoki maxsus URLga yo'naltirsa (masalan, /yangiliklar/), shu yerga kiriting. 'Link to Page' tanlangan bo'lsa, bu bo'sh qoldiriladi."))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True, verbose_name=_("Parent Item"))
    order = models.PositiveIntegerField(_("Order"), default=0)
    MENU_LOCATIONS = [
        ('main_menu', _('Main Menu (Header)')),
        ('footer_menu', _('Footer Menu')),
    ]
    location = models.CharField(
        _("Menu Location"),
        max_length=50,
        choices=MENU_LOCATIONS,
        default='main_menu',
        help_text=_("Bu menyu bandi qaysi menyuda ko'rinishi kerak.")
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.title or _("Nomsiz Menyu Bandi")

    def get_link(self):
        if self.link_page:
            try:
                return self.link_page.get_absolute_url()
            except Exception:
                return "#page-not-found-or-no-translation"
        elif self.link_url:
            return self.link_url
        return "#"