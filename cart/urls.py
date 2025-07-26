# cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # 🛒 عرض سلة التسوق
    path('', views.cart_view, name='cart'),

    # ➕ إضافة منتج للسلة (عادي)
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # ⚡ إضافة منتج للسلة باستخدام Ajax
    path('ajax/add/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),

    # 🔼 زيادة كمية منتج
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),

    # 🔽 تقليل كمية منتج
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),

    # ❌ إزالة منتج من السلة
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 🧺 تفريغ السلة بالكامل
    path('clear/', views.clear_cart, name='clear_cart'),

    # 🎟️ تطبيق كود خصم
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]
