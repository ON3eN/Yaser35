# cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),  # 🛒 عرض السلة
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # ➕ إضافة منتج إلى السلة (عادي)
    path('ajax/add/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),  # ⚡ إضافة منتج باستخدام Ajax
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),  # 🔼 زيادة الكمية
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),  # 🔽 تقليل الكمية
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # ❌ إزالة منتج من السلة
    path('clear/', views.clear_cart, name='clear_cart'),  # 🧺 تفريغ السلة
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),  # 🎟️ تطبيق كود الخصم
]
