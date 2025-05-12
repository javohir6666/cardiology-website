# doctors/views.py
from django.views.generic import ListView # DetailView ni keyinroq qo'shishimiz mumkin
from .models import Doctor
# from django.utils.translation import gettext_lazy as _ # Agar viewda tarjima kerak bo'lsa

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 12 # Bir sahifada nechta shifokor

    def get_queryset(self):
        # Faqat aktiv shifokorlarni olish va tartib bo'yicha saralash
        # `prefetch_related` tarjimalarni olishda yordam beradi
        return Doctor.objects.filter(is_active=True).prefetch_related('translations').order_by('order', 'translations__full_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Bizning Shifokorlar' # Tarjima qilinishi mumkin
        # Bu yerga ixtisosliklar bo'yicha filter qo'shish mumkin, agar Doctor modelida
        # ixtisoslik (specialty) alohida model yoki aniq tanlovlar bilan berilgan bo'lsa.
        # Masalan: context['specialties'] = DoctorSpecialty.objects.all()
        return context

# Agar DoctorDetailView kerak bo'lsa (kelajakda):
# from parler.views import TranslatableSlugMixin # Agar slug bilan ishlasak
# class DoctorDetailView(DetailView): # Yoki TranslatableSlugMixin bilan birga
#     model = Doctor
#     template_name = 'doctors/doctor_detail.html'
#     context_object_name = 'doctor'
#     # slug_field = 'slug' # Agar slug ishlatilsa va TranslatableSlugMixin bilan
#     # pk_url_kwarg = 'pk' # Agar pk ishlatilsa (standart)

#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True).prefetch_related('translations')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = self.object.safe_translation_getter('full_name', any_language=True)
#         return context