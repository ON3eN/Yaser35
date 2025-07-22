# account/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('register/', views.register_view, name='register'),        # إنشاء حساب جديد
    path('login/', views.login_view, name='login'),                 # تسجيل الدخول
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # تسجيل الخروج وإعادة التوجيه للرئيسية
]
