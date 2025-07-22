from django.urls import path
from . import views  # استيراد الفيوز

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),  # الصفحة الرئيسية
    path('products/', views.products_page, name='products'),  # صفحة المنتجات فقط
]
