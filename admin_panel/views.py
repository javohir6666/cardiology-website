from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import render, redirect
from news.models import News
from pages.models import Page
from publications.models import Publication
from doctors.models import Doctor
from core.models import GalleryImage
from .forms import NewsForm, PageForm, PublicationForm, DoctorForm, GalleryForm

class AdminLoginView(LoginView):
    template_name = 'admin_panel/login.html'
    redirect_authenticated_user = True

class AdminLogoutView(LogoutView):
    next_page = '/admin/login/'

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

# News CRUD
class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'admin_panel/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

def news_create(request):
    language_codes = [lang[0] for lang in settings.LANGUAGES]
    forms = {}
    if request.method == 'POST':
        is_valid = True
        for lang in language_codes:
            forms[lang] = NewsForm(request.POST, request.FILES, prefix=lang)
            if not forms[lang].is_valid():
                is_valid = False
        if is_valid:
            obj = News()
            # Umumiy maydonlar (faqat default til formidan)
            main_form = forms[settings.LANGUAGES[0][0]]
            for field in ['image', 'category', 'is_published']:
                if field in main_form.cleaned_data:
                    setattr(obj, field, main_form.cleaned_data[field])
            obj.save()
            # Har bir til uchun TranslatedFields
            for lang in language_codes:
                form = forms[lang]
                obj.set_current_language(lang)
                for field in ['title', 'slug', 'content', 'keywords']:
                    if field in form.cleaned_data:
                        setattr(obj, field, form.cleaned_data[field])
                obj.save()
            return redirect('admin_panel:news_list')
    else:
        for lang in language_codes:
            forms[lang] = NewsForm(prefix=lang)
    return render(request, 'admin_panel/news_form.html', {
        'forms': forms,
        'LANGUAGES': settings.LANGUAGES,
    })

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_panel/news_form.html'
    success_url = reverse_lazy('admin_panel:news_list')

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'admin_panel/news_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:news_list')

# Page CRUD
class PageListView(LoginRequiredMixin, ListView):
    model = Page
    template_name = 'admin_panel/page_list.html'
    context_object_name = 'page_list'
    paginate_by = 10

def page_create(request):
    language_codes = [lang[0] for lang in settings.LANGUAGES]
    forms = {}
    if request.method == 'POST':
        is_valid = True
        for lang in language_codes:
            forms[lang] = PageForm(request.POST, request.FILES, prefix=lang)
            if not forms[lang].is_valid():
                is_valid = False
        if is_valid:
            obj = Page()
            # Umumiy maydonlar (faqat default til formidan)
            main_form = forms[settings.LANGUAGES[0][0]]
            for field in ['template_name', 'is_published']:
                if field in main_form.cleaned_data:
                    setattr(obj, field, main_form.cleaned_data[field])
            obj.save()
            # Har bir til uchun TranslatedFields
            for lang in language_codes:
                form = forms[lang]
                obj.set_current_language(lang)
                for field in ['title', 'slug', 'content', 'meta_keywords', 'meta_description']:
                    if field in form.cleaned_data:
                        setattr(obj, field, form.cleaned_data[field])
                obj.save()
            return redirect('admin_panel:page_list')
    else:
        for lang in language_codes:
            forms[lang] = PageForm(prefix=lang)
    return render(request, 'admin_panel/page_form.html', {
        'forms': forms,
        'LANGUAGES': settings.LANGUAGES,
    })

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'admin_panel/page_form.html'
    success_url = reverse_lazy('admin_panel:page_list')

class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'admin_panel/page_form.html'
    success_url = reverse_lazy('admin_panel:page_list')

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'admin_panel/page_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:page_list')

# Publication CRUD
class PublicationListView(LoginRequiredMixin, ListView):
    model = Publication
    template_name = 'admin_panel/publication_list.html'
    context_object_name = 'publication_list'
    paginate_by = 10

def publication_create(request):
    language_codes = [lang[0] for lang in settings.LANGUAGES]
    forms = {}
    if request.method == 'POST':
        is_valid = True
        for lang in language_codes:
            forms[lang] = PublicationForm(request.POST, request.FILES, prefix=lang)
            if not forms[lang].is_valid():
                is_valid = False
        if is_valid:
            obj = Publication()
            # Umumiy maydonlar (faqat default til formidan)
            main_form = forms[settings.LANGUAGES[0][0]]
            for field in ['authors', 'category', 'cover_image', 'file', 'publication_year', 'publisher', 'is_published']:
                if field in main_form.cleaned_data:
                    setattr(obj, field, main_form.cleaned_data[field])
            obj.save()
            # Har bir til uchun TranslatedFields
            for lang in language_codes:
                form = forms[lang]
                obj.set_current_language(lang)
                for field in ['title', 'slug', 'short_description', 'content']:
                    if field in form.cleaned_data:
                        setattr(obj, field, form.cleaned_data[field])
                obj.save()
            return redirect('admin_panel:publication_list')
    else:
        for lang in language_codes:
            forms[lang] = PublicationForm(prefix=lang)
    return render(request, 'admin_panel/publication_form.html', {
        'forms': forms,
        'LANGUAGES': settings.LANGUAGES,
    })

class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'admin_panel/publication_form.html'
    success_url = reverse_lazy('admin_panel:publication_list')

class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    template_name = 'admin_panel/publication_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:publication_list')

# Doctor CRUD
class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'admin_panel/doctor_list.html'
    context_object_name = 'doctor_list'
    paginate_by = 10

def doctor_create(request):
    language_codes = [lang[0] for lang in settings.LANGUAGES]
    forms = {}
    if request.method == 'POST':
        is_valid = True
        for lang in language_codes:
            forms[lang] = DoctorForm(request.POST, request.FILES, prefix=lang)
            if not forms[lang].is_valid():
                is_valid = False
        if is_valid:
            obj = Doctor()
            # Umumiy maydonlar (faqat default til formidan)
            main_form = forms[settings.LANGUAGES[0][0]]
            for field in ['photo', 'email', 'phone', 'experience_years', 'is_active', 'order']:
                if field in main_form.cleaned_data:
                    setattr(obj, field, main_form.cleaned_data[field])
            obj.save()
            # Har bir til uchun TranslatedFields
            for lang in language_codes:
                form = forms[lang]
                obj.set_current_language(lang)
                for field in ['full_name', 'position', 'bio']:
                    if field in form.cleaned_data:
                        setattr(obj, field, form.cleaned_data[field])
                obj.save()
            return redirect('admin_panel:doctor_list')
    else:
        for lang in language_codes:
            forms[lang] = DoctorForm(prefix=lang)
    return render(request, 'admin_panel/doctor_form.html', {
        'forms': forms,
        'LANGUAGES': settings.LANGUAGES,
    })

class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'admin_panel/doctor_form.html'
    success_url = reverse_lazy('admin_panel:doctor_list')

class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'admin_panel/doctor_form.html'
    success_url = reverse_lazy('admin_panel:doctor_list')

class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'admin_panel/doctor_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:doctor_list')

# Gallery CRUD
class GalleryListView(LoginRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'admin_panel/gallery_list.html'
    context_object_name = 'gallery_list'
    paginate_by = 12

def gallery_create(request):
    language_codes = [lang[0] for lang in settings.LANGUAGES]
    forms = {}
    if request.method == 'POST':
        is_valid = True
        for lang in language_codes:
            forms[lang] = GalleryForm(request.POST, request.FILES, prefix=lang)
            if not forms[lang].is_valid():
                is_valid = False
        if is_valid:
            obj = GalleryImage()
            # Umumiy maydonlar (faqat default til formidan)
            main_form = forms[settings.LANGUAGES[0][0]]
            for field in ['image']:
                if field in main_form.cleaned_data:
                    setattr(obj, field, main_form.cleaned_data[field])
            obj.save()
            # Har bir til uchun TranslatedFields
            for lang in language_codes:
                form = forms[lang]
                obj.set_current_language(lang)
                for field in ['title']:
                    if field in form.cleaned_data:
                        setattr(obj, field, form.cleaned_data[field])
                obj.save()
            return redirect('admin_panel:gallery_list')
    else:
        for lang in language_codes:
            forms[lang] = GalleryForm(prefix=lang)
    return render(request, 'admin_panel/gallery_form.html', {
        'forms': forms,
        'LANGUAGES': settings.LANGUAGES,
    })

class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryImage
    form_class = GalleryForm
    template_name = 'admin_panel/gallery_form.html'
    success_url = reverse_lazy('admin_panel:gallery_list')

class GalleryUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryImage
    form_class = GalleryForm
    template_name = 'admin_panel/gallery_form.html'
    success_url = reverse_lazy('admin_panel:gallery_list')

class GalleryDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryImage
    template_name = 'admin_panel/gallery_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:gallery_list')
