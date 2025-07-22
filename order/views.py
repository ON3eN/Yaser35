# order/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Order

@login_required
def process_order(request):
    cart = request.session.get('cart_items', [])
    if not cart:
        messages.error(request, "السلة فارغة")
        return redirect('cart:cart')

    for item in cart:
        try:
            product = Product.objects.get(name=item['name'])
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=1  # أو item['quantity'] إذا تدعم كميات
            )
        except Product.DoesNotExist:
            continue

    # تفريغ السلة
    request.session['cart_items'] = []

    messages.success(request, "تم إتمام الشراء بنجاح!")
    return redirect('home')
