from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'

urlpatterns = [
    # صفحات التسجيل وتسجيل الدخول
    path('register/', views.register_view, name='register'),
    path('signup/', views.register_view, name='signup'),  # اسم إضافي للتسجيل
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # إعدادات الحساب والدفع
    path('settings/', views.account_settings, name='account_settings'),
    path('payment-settings/', views.payment_settings, name='payment_settings'),
]
