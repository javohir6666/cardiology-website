from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field

class Doctor(TranslatableModel):
    translations = TranslatedFields(
        full_name = models.CharField(_("Full Name"), max_length=255),
        position = models.CharField(_("Position/Specialty"), max_length=200),
        bio = CKEditor5Field(_("Biography/Additional Information"), blank=True, null=True)
    )
    photo = models.ImageField(_("Photo"), upload_to='doctors_photos/%Y/%m/')
    email = models.EmailField(_("Email"), max_length=255, blank=True, null=True)
    phone = models.CharField(_("Phone Number"), max_length=50, blank=True, null=True)
    experience_years = models.PositiveIntegerField(_("Years of Experience"), blank=True, null=True)
    # Siz aytgan qabul kunlari va vaqtlarini ham qo'shish mumkin (CharField yoki alohida model)
    # consultation_hours = models.CharField(_("Consultation Hours"), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(_("Is Active Staff"), default=True) # Saytda ko'rsatish/ko'rsatmaslik
    order = models.PositiveIntegerField(_("Order"), default=0, help_text=_("Ro'yxatda chiqish tartibi"))


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        ordering = ['order', 'translations__full_name'] # Order bo'yicha, keyin ism bo'yicha

    def __str__(self):
        return self.safe_translation_getter("full_name", any_language=True) or _("Nomsiz Shifokor")