from django.urls import path
from . import views  # استيراد جميع الفيوز من التطبيق

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),                 # عرض الصفحة الرئيسية
    path('products/', views.products_page, name='products'),  # عرض صفحة المنتجات فقط
]
