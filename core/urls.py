# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    # Boshqa umumiy sahifalar uchun URL'lar (masalan, bog'lanish sahifasi, agar alohida ilovada bo'lmasa)
    path('gallery/', views.gallery_view, name='gallery'),
]