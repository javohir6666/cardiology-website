from django.urls import path
from . import views
from .views import AdminLoginView, AdminLogoutView, AdminDashboardView

app_name = 'admin_panel'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', AdminLogoutView.as_view(), name='logout'),
    # News CRUD
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    # Page CRUD
    path('pages/', views.PageListView.as_view(), name='page_list'),
    path('pages/create/', views.page_create, name='page_create'),
    path('pages/<int:pk>/edit/', views.PageUpdateView.as_view(), name='page_edit'),
    path('pages/<int:pk>/delete/', views.PageDeleteView.as_view(), name='page_delete'),
    # Publication CRUD
    path('publications/', views.PublicationListView.as_view(), name='publication_list'),
    path('publications/create/', views.publication_create, name='publication_create'),
    path('publications/<int:pk>/edit/', views.PublicationUpdateView.as_view(), name='publication_edit'),
    path('publications/<int:pk>/delete/', views.PublicationDeleteView.as_view(), name='publication_delete'),
    # Doctor CRUD
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    # Gallery CRUD
    path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/<int:pk>/edit/', views.GalleryUpdateView.as_view(), name='gallery_edit'),
    path('gallery/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),
]
