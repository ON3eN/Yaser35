from django.shortcuts import render
from .models import Product  # استيراد موديل المنتجات

def home(request):
    # جلب المنتجات المتوفرة فقط، مرتبة من الأحدث
    products = Product.objects.filter(available=True).order_by('-created_at')

    # اسم المستخدم (إذا كان مسجلاً دخوله)
    username = request.user.username if request.user.is_authenticated else ''

    # تمرير البيانات إلى قالب الصفحة الرئيسية
    return render(request, 'home.html', {
        'products': products,
        'username': username,
        'request': request  # ضروري لتمييز الصفحة الرئيسية في القالب
    })

def products_page(request):
    # جلب المنتجات المتوفرة فقط، مرتبة من الأحدث
    products = Product.objects.filter(available=True).order_by('-created_at')

    # تمرير المنتجات فقط لقالب المنتجات
    return render(request, 'products.html', {
        'products': products,
        'request': request  # في حال احتجت تمييز التصميم أو إدراج إضافات
    })
