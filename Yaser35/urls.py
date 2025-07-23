from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from store.views import home  # عرض الصفحة الرئيسية

urlpatterns = [
    # لوحة التحكم
    path('admin/', admin.site.urls),

    # الصفحة الرئيسية
    path('', home, name='home'),

    # روابط التطبيقات
    path('store/', include('store.urls', namespace='store')),  # المنتجات
    path('order/', include('order.urls', namespace='order')),  # الطلبات
    path('account/', include('account.urls')),                 # الحساب (تسجيل دخول، تسجيل، خروج)
    path('cart/', include('cart.urls')),                       # السلة
]

# دعم عرض ملفات media في بيئة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
