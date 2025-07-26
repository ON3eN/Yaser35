# order/urls.py

# مسارات الطلبات - تطبيق order
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),  # ✅ صفحة إتمام الطلب
]
