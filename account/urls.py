from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('signup/', views.register_view, name='signup'),  # اختياري لدعم alias في صفحات أخرى
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
