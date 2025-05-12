# doctors/urls.py
from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    # Agar har bir shifokor uchun alohida sahifa kerak bo'lsa, keyinroq qo'shamiz:
    # path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    # Yoki slug bilan:
    # path('<slug:slug>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
]