# order/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Order

@login_required
def process_order(request):
    # جلب محتوى السلة من الجلسة
    cart = request.session.get('cart_items', [])

    # تحقق إن السلة غير فارغة
    if not cart:
        messages.error(request, "السلة فارغة")
        return redirect('cart:cart')

    # إنشاء الطلبات بناءً على محتوى السلة
    for item in cart:
        try:
            product = Product.objects.get(id=item['id'])  # الأفضل استخدام ID بدل الاسم
            quantity = item.get('quantity', 1)

            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )
        except Product.DoesNotExist:
            # تجاوز المنتج إذا ما كان موجود
            continue

    # تفريغ السلة بعد إتمام الطلب
    request.session['cart_items'] = []

    # رسالة نجاح
    messages.success(request, "تم إتمام الشراء بنجاح!")

    # إعادة التوجيه للصفحة الرئيسية
    return redirect('home')
