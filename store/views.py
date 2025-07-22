from django.shortcuts import render
from .models import Product  # استيراد موديل المنتجات

def home(request):
    # جلب المنتجات المتوفرة فقط، مرتبة من الأحدث
    products = Product.objects.filter(available=True).order_by('-created_at')
    
    # تمرير المنتجات إلى قالب home.html
    return render(request, 'home.html', {'products': products})
