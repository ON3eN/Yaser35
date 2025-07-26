# store/urls.py

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.products_page, name='products'),   # عرض جميع المنتجات
]
