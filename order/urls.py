# order/urls.py
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.process_order, name='process_order'),  # ✅ هذا هو المسار المستخدم في cart.html
]
