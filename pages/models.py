from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager, TranslatableQuerySet # TranslatableQuerySet ni import qilamiz
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager # TreeManager ni import qilamiz
from mptt.querysets import TreeQuerySet # TreeQuerySet ni import qilamiz

class Page(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("Page Title"), max_length=255),
        slug = models.SlugField(_("Slug (URL)"), max_length=270, unique=True, help_text=_("Sahifaning URL manzili, masalan 'biz-haqimizda'. Agar bo'sh qoldirilsa, sarlavhadan avtomatik generatsiya qilinadi.")),
        content = CKEditor5Field(_("Page Content"), config_name='default'),
        meta_keywords = models.CharField(_("Meta Keywords"), max_length=255, blank=True, null=True, help_text=_("SEO uchun kalit so'zlar, vergul bilan ajratilgan.")),
        meta_description = models.TextField(_("Meta Description"), blank=True, null=True, help_text=_("SEO uchun sahifa tavsifi."))
    )
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
        return self.safe_translation_getter("title", any_language=True) or _("Nomsiz Sahifa")

    def save(self, *args, **kwargs):
        # Slugni avtomatik generatsiya qilish logikasi
        # Har bir til uchun alohida slug generatsiya qilishni o'ylab ko'rish kerak
        # Hozirgi holatda, agar slug bo'sh bo'lsa, joriy tildagi sarlavhadan generatsiya qiladi
        # Bu xatti-harakatni parler sozlamalari bilan ham boshqarish mumkin
        current_language = self.get_current_language()
        if not self.safe_translation_getter('slug', language_code=current_language, any_language=False) and \
           self.safe_translation_getter('title', language_code=current_language, any_language=False):
            new_slug = slugify(self.safe_translation_getter('title', language_code=current_language))
            # Agar bunday slug boshqa tilda yoki boshqa obyektda mavjud bo'lsa, unikal qilish kerak bo'lishi mumkin
            self.set_current_language(current_language)
            self.slug = new_slug # Bu joriy til uchun slugni o'rnatadi
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            # Joriy tildagi slugni olishga harakat qilamiz
            current_slug = self.safe_translation_getter('slug', language_code=self.get_current_language())
            if not current_slug: # Agar joriy tilda slug bo'lmasa, birinchi mavjud slugni olamiz
                current_slug = self.safe_translation_getter('slug', any_language=True)
            
            if current_slug: # Agar slug mavjud bo'lsa
                 return reverse('pages:page_detail', kwargs={'slug': current_slug})
            else: # Agar hech qanday slug topilmasa (bu holat bo'lmasligi kerak)
                 return "/" # Yoki xatolik sahifasiga yo'naltirish
        except Exception:
            return "/"


# MPTT va Parler uchun maxsus QuerySet
class MenuItemQuerySet(TreeQuerySet, TranslatableQuerySet):
    pass

# MPTT va Parler uchun maxsus Manager
class MenuItemManager(TreeManager, TranslatableManager):
    _queryset_class = MenuItemQuerySet # Maxsus QuerySet ni ishlatish

    # Agar TreeManager va TranslatableManager da bir xil nomli metodlar bo'lsa,
    # ularni to'g'ri chaqirish uchun super() ni ehtiyotkorlik bilan ishlatish kerak bo'lishi mumkin.
    # Hozircha standart implementatsiya yetarli bo'lishi kerak.


class MenuItem(MPTTModel, TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("Menu Item Title"), max_length=100)
    )
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

    # Maxsus manager'ni modelga biriktirish
    objects = MenuItemManager()

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or _("Nomsiz Menyu Bandi")

    def get_link(self):
        if self.link_page:
            try:
                # link_page allaqachon to'g'ri tilda bo'lishi kerak (agar parler to'g'ri ishlayotgan bo'lsa)
                # get_absolute_url ham joriy tilni hisobga olishi kerak
                return self.link_page.get_absolute_url()
            except Exception:
                return "#page-not-found-or-no-translation"
        elif self.link_url:
            # Agar link_url ham tilga bog'liq bo'lishi kerak bo'lsa, bu yerda qo'shimcha logika kerak
            # Masalan, agar link_url "/%s/some/path/" % get_language() kabi bo'lsa
            return self.link_url
        return "#"