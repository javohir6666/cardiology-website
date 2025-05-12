# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Bu URL boshqa ilovalarning URL'laridan keyin turishi kerak,
    # chunki u umumiyroq bo'lib, boshqa aniq URL'larni "yutib yuborishi" mumkin.
    # Asosiy cardio_project/urls.py da i18n_patterns ichida eng oxirida qo'ygan ma'qul.
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]