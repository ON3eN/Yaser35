# store/views.py

from django.shortcuts import render
from .models import Product  # استيراد موديل المنتجات

# ✅ عرض الصفحة الرئيسية
def home(request):
    # جلب أول 3 منتجات متوفرة فقط، مرتبة من الأحدث
    latest_products = Product.objects.filter(available=True).order_by('-created_at')[:3]

    # معرفة المستخدم الحالي (إن وجد)
    username = request.user.username if request.user.is_authenticated else ''

    return render(request, 'home.html', {
        'products': latest_products,
        'username': username,
        'request': request
    })

# ✅ عرض صفحة كل المنتجات
def products_page(request):
    # جلب جميع المنتجات المتوفرة
    all_products = Product.objects.filter(available=True).order_by('-created_at')

    return render(request, 'products.html', {
        'products': all_products,
        'request': request
    })
