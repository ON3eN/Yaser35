from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

# عرض السلة
def cart_view(request):
    # جلب العناصر من الجلسة أو قائمة فاضية
    cart_items = request.session.get('cart_items', [])
    
    # حساب المجموع
    total = sum(item['price'] for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

# إضافة منتج إلى السلة
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # بناء عنصر السلة
    item = {
        'id': product.id,
        'name': product.name,
        'price': float(product.price),  # نحوله إلى float لأنه Decimal
    }

    # جلب السلة من الجلسة أو تهيئتها
    cart_items = request.session.get('cart_items', [])
    cart_items.append(item)
    request.session['cart_items'] = cart_items

    return redirect('cart:cart')  # ✅ هذا هو الصحيح

