from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class GalleryImage(models.Model):
    image = models.ImageField(_('Rasm'), upload_to='gallery/')
    title = models.CharField(_('Rasm nomi'), max_length=255, blank=True)
    uploaded_at = models.DateTimeField(_('Yuklangan vaqti'), auto_now_add=True)

    class Meta:
        verbose_name = _('Galereya rasmi')
        verbose_name_plural = _('Galereya rasmlari')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or str(self.image)
