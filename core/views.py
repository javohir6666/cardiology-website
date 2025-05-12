# core/views.py
from django.shortcuts import render
from news.models import News # Bosh sahifada yangiliklarni chiqarish uchun
from doctors.models import Doctor # Bosh sahifada shifokorlarni chiqarish uchun (masalan, bir nechtasini)
from core.models import GalleryImage

app_name = 'core'

def home_page_view(request):
    # Carousel uchun 3 ta eng so'nggi yangilik
    carousel_news = News.objects.filter(is_published=True).prefetch_related('translations')[:3]
    # 8 ta yangilik (cardlar uchun)
    # news_cards = News.objects.filter(is_published=True).prefetch_related('translations')[3:11]
    news_cards = News.objects.filter(is_published=True).prefetch_related('translations')[:8]
    # 4 ta shifokor
    featured_doctors = Doctor.objects.filter(is_active=True).prefetch_related('translations')[:4]

    context = {
        'carousel_news': carousel_news,
        'news_cards': news_cards,
        'featured_doctors': featured_doctors,
        'page_title': 'Bosh sahifa'
    }
    return render(request, 'core/home.html', context)

def gallery_view(request):
    images = GalleryImage.objects.all()
    context = {
        'images': images,
        'page_title': 'Galereya'
    }
    return render(request, 'core/gallery.html', context)