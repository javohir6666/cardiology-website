# cardio_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns # Ko'p tilli URLlar uchun

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # CKEditor5 upload URL
    # path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')), # Tilni o'zgartirish uchun standart URL
]

# Ko'p tilli bo'ladigan URL'lar (saytning asosiy qismi)
urlpatterns += i18n_patterns(
    path('', include('core.urls', namespace='core')), # Asosiy sahifa va boshqa core URL'lar
    path('news/', include('news.urls', namespace='news')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('publications/', include('publications.urls', namespace='publications')),
    path('pages/', include('pages.urls', namespace='pages')), # Dinamik sahifalar va menyu bilan bog'liq URL'lar
    # prefix_default_language=False # Agar standart til uchun prefiks (/uz/) kerak bo'lmasa
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Agar STATIC_ROOT ishlatilsa