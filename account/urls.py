# account/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'

urlpatterns = [
    # 📝 صفحات التسجيل وتسجيل الدخول
    path('register/', views.register_view, name='register'),           # إنشاء حساب
    path('signup/', views.register_view, name='signup'),               # اسم بديل لإنشاء حساب
    path('login/', views.login_view, name='login'),                    # تسجيل الدخول
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # تسجيل الخروج

    # ⚙️ إعدادات الحساب
    path('settings/', views.account_settings, name='account_settings'),  # إعدادات الحساب
    path('payment-settings/', views.payment_settings, name='payment_settings'),  # إعدادات الدفع
]
