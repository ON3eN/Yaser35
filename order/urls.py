# order/urls.py
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.process_order, name='checkout'),  # ✅ هذا الجديد
]
