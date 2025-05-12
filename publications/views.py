# publications/views.py
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Publication, PublicationCategory
from parler.views import TranslatableSlugMixin
# from django.utils.translation import gettext_lazy as _

class PublicationListView(ListView):
    model = Publication
    template_name = 'publications/publication_list.html'
    context_object_name = 'publications'
    paginate_by = 10 # Bir sahifada nechta nashr

    def get_queryset(self):
        queryset = Publication.objects.filter(is_published=True).prefetch_related('translations', 'category__translations')
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            try:
                category = PublicationCategory.objects.translated(slug=category_slug).first()
                if category:
                    queryset = queryset.filter(category=category)
            except PublicationCategory.DoesNotExist:
                pass
        return queryset.order_by('-publication_year', 'translations__title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nashrlar' # Tarjima qilinishi mumkin
        context['categories'] = PublicationCategory.objects.all().prefetch_related('translations')
        return context

class PublicationDetailView(TranslatableSlugMixin, DetailView):
    model = Publication
    template_name = 'publications/publication_detail.html'
    context_object_name = 'publication'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).prefetch_related('translations', 'category__translations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.safe_translation_getter('title', any_language=True)
        return context

def download_publication_view(request, pk):
    publication = get_object_or_404(Publication, pk=pk, is_published=True)
    
    # Fayl mavjudligini tekshirish
    if not publication.file:
        raise Http404("Fayl topilmadi.")

    # Yuklab olishlar sonini oshirish
    publication.downloads_count += 1
    publication.save(update_fields=['downloads_count'])
    
    # Faylni FileResponse orqali qaytarish
    # 'as_attachment=True' brauzerga faylni ko'rsatish o'rniga yuklab olishni taklif qiladi
    try:
        response = FileResponse(publication.file.open('rb'), as_attachment=True, filename=publication.file.name.split('/')[-1])
        return response
    except FileNotFoundError:
        raise Http404("Fayl serverda topilmadi.")
    except Exception as e: # Boshqa xatoliklarni tutish
        # Log yozish yoki xatolik haqida xabar berish
        # Soddalashtirilgan xatolik:
        raise Http404(f"Faylni yuklashda xatolik: {e}")