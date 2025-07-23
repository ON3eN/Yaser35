# store/views.py
from django.shortcuts import render
from .models import Product  # استيراد موديل المنتجات

# الصفحة الرئيسية
def home(request):
    # جلب أول 3 منتجات متوفرة فقط، مرتبة من الأحدث
    products = Product.objects.filter(available=True).order_by('-created_at')[:3]

    # اسم المستخدم (إذا كان مسجلاً دخوله)
    username = request.user.username if request.user.is_authenticated else ''

    # تمرير البيانات إلى قالب الصفحة الرئيسية
    return render(request, 'home.html', {
        'products': products,
        'username': username,
        'request': request  # للتمييز داخل القالب
    })

# صفحة المنتجات المفصولة
def products_page(request):
    # جلب كل المنتجات المتوفرة، مرتبة من الأحدث
    products = Product.objects.filter(available=True).order_by('-created_at')

    # تمرير البيانات لقالب صفحة المنتجات
    return render(request, 'products.html', {
        'products': products,
        'request': request
    })
