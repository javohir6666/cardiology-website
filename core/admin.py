from django.contrib import admin
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image', 'uploaded_at')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)
