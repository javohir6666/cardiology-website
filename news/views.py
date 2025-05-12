# news/views.py
from django.views.generic import ListView, DetailView
from .models import News, NewsCategory
from parler.views import TranslatableSlugMixin # Tarjima qilingan sluglar uchun

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_items'
    paginate_by = 9 # Bir sahifada nechta yangilik ko'rsatilishi

    def get_queryset(self):
        # Faqat chop etilgan va joriy til uchun tarjimasi bor yangiliklarni olish
        # Parler buni avtomatik qiladi, agar model to'g'ri sozlangan bo'lsa
        # Lekin ishonch hosil qilish uchun .active_translations() dan foydalanish mumkin
        # queryset = News.objects.active_translations(get_language()).filter(is_published=True)
        queryset = News.objects.filter(is_published=True).prefetch_related('translations', 'category__translations')
        
        # Kategoriya bo'yicha filterlash (agar URLda category slug bo'lsa)
        category_slug = self.request.GET.get('category')
        if category_slug:
            # Bu yerda NewsCategory ni ham TranslatableSlugMixin bilan olish kerak bo'lishi mumkin
            # Yoki to'g'ridan-to'g'ri translations orqali filter qilish
            try:
                # NewsCategory.objects.language(get_language()).get(slug=category_slug)
                # Yoki agar slug barcha tillar uchun bir xil bo'lsa:
                category = NewsCategory.objects.translated(slug=category_slug).first()
                if category:
                    queryset = queryset.filter(category=category)
            except NewsCategory.DoesNotExist:
                pass # Yoki xatolikni qaytarish
        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Yangiliklar' # Buni tarjima qilish mumkin
        context['categories'] = NewsCategory.objects.all().prefetch_related('translations') # Filterlash uchun kategoriyalar
        return context

class NewsDetailView(TranslatableSlugMixin, DetailView): # TranslatableSlugMixin slugni to'g'ri tilida topishga yordam beradi
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    # slug_field = 'slug' # Bu TranslatableSlugMixin uchun kerak emas, modelda topiladi
    # slug_url_kwarg = 'slug' # Bu ham standart

    def get_queryset(self):
        # Faqat chop etilgan yangiliklarni olish
        # TranslatableSlugMixin o'zi kerakli tildagi obyektni topishga harakat qiladi
        return super().get_queryset().filter(is_published=True).prefetch_related('translations', 'category__translations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # `object` allaqachon TranslatableSlugMixin tomonidan to'g'ri tilda topilgan bo'ladi
        context['page_title'] = self.object.safe_translation_getter('title', any_language=True)
        
        # Ko'rishlar sonini oshirish (oddiy usul)
        news = self.object
        news.views_count += 1
        news.save(update_fields=['views_count']) # Faqat shu maydonni yangilash
        
        return context