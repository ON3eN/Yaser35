# Yaser35/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import home  # عرض الصفحة الرئيسية

urlpatterns = [
    # 🔧 لوحة التحكم
    path('admin/', admin.site.urls),

    # 🏠 الصفحة الرئيسية
    path('', home, name='home'),

    # 🛍️ روابط التطبيقات
    path('store/', include(('store.urls', 'store'), namespace='store')),     # المنتجات
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),         # السلة
    path('order/', include(('order.urls', 'order'), namespace='order')),     # الطلبات
    path('account/', include(('account.urls', 'account'), namespace='account')),  # الحسابات
]

# 🖼️ دعم تحميل ملفات media أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
