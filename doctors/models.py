from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

class Doctor(models.Model):
    full_name = models.CharField(_("Full Name"), max_length=255)
    position = models.CharField(_("Position/Specialty"), max_length=200)
    bio = CKEditor5Field(_("Biography/Additional Information"), blank=True, null=True)
    photo = models.ImageField(_("Photo"), upload_to='doctors_photos/%Y/%m/')
    email = models.EmailField(_("Email"), max_length=255, blank=True, null=True)
    phone = models.CharField(_("Phone Number"), max_length=50, blank=True, null=True)
    experience_years = models.PositiveIntegerField(_("Years of Experience"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active Staff"), default=True)
    order = models.PositiveIntegerField(_("Order"), default=0, help_text=_("Ro'yxatda chiqish tartibi"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        ordering = ['order', 'full_name']

    def __str__(self):
        return self.full_name or _("Nomsiz Shifokor")