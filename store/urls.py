# store/urls.py

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),                      # 🏠 الصفحة الرئيسية (تظهر 3 منتجات فقط)
    path('products/', views.products_page, name='products') # 🛍️ عرض جميع المنتجات
]
