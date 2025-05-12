# publications/urls.py
from django.urls import path
from . import views

app_name = 'publications'

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='publication_list'),
    path('<slug:slug>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('download/<int:pk>/', views.download_publication_view, name='publication_download'), # Faylni yuklab olish uchun maxsus view
]