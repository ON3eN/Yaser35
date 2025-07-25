from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# ✅ عرض السلة
def cart_view(request):
    cart_items = request.session.get('cart_items', [])
    discount = request.session.get('discount', 0)

    for item in cart_items:
        item['quantity'] = item.get('quantity', 1)
        item['subtotal'] = round(item['price'] * item['quantity'], 2)

        # ضمان وجود رابط الصورة من الموديل
        if 'image_url' not in item or not item['image_url']:
            try:
                product = Product.objects.get(id=item['id'])
                item['image_url'] = product.image.url if product.image else ''
            except Product.DoesNotExist:
                item['image_url'] = ''

    total = sum(item['subtotal'] for item in cart_items)
    discounted_total = round(total * (1 - discount), 2)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': round(total, 2),
        'discount': discount,
        'discounted_total': discounted_total if discount else None,
    })

# ✅ إضافة منتج إلى السلة (عادي)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_items = request.session.get('cart_items', [])

    for item in cart_items:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image_url': product.image.url if product.image else "",
        })

    request.session['cart_items'] = cart_items
    messages.success(request, f"✅ تمت إضافة {product.name} إلى السلة 🛒")
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

# ✅ إضافة منتج باستخدام Ajax
@require_POST
def ajax_add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_items = request.session.get('cart_items', [])

    for item in cart_items:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image_url': product.image.url if product.image else "",
        })

    request.session['cart_items'] = cart_items

    return JsonResponse({
        'message': f"✅ تمت إضافة {product.name} إلى السلة 🛒",
        'cartCount': sum(item['quantity'] for item in cart_items)
    })

# ✅ زيادة الكمية
def increase_quantity(request, product_id):
    cart_items = request.session.get('cart_items', [])
    for item in cart_items:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    request.session['cart_items'] = cart_items
    return redirect('cart:cart_detail')

# ✅ تقليل الكمية مع تنبيه المستخدم
def decrease_quantity(request, product_id):
    cart_items = request.session.get('cart_items', [])
    for item in cart_items:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                messages.warning(request, "📌 إذا كنت تريد حذف المنتج، اضغط على علامة الحذف الحمراء.")
            break
    request.session['cart_items'] = cart_items
    return redirect('cart:cart_detail')

# ✅ إزالة منتج من السلة
def remove_from_cart(request, product_id):
    cart_items = request.session.get('cart_items', [])
    cart_items = [item for item in cart_items if item['id'] != product_id]
    request.session['cart_items'] = cart_items
    messages.info(request, "🗑️ تمت إزالة المنتج من السلة")
    return redirect('cart:cart_detail')

# ✅ تفريغ السلة
def clear_cart(request):
    request.session['cart_items'] = []
    request.session['discount'] = 0
    messages.info(request, "🧺 تم تفريغ السلة بنجاح")
    return redirect('cart:cart_detail')

# ✅ تطبيق كود الخصم
@require_POST
def apply_coupon(request):
    code = request.POST.get('coupon_code', '').strip().lower()

    if code == 'خصم10':
        request.session['discount'] = 0.10
        messages.success(request, "🎉 تم تطبيق كود الخصم 10%")
    else:
        request.session['discount'] = 0
        messages.warning(request, "❌ كود الخصم غير صالح")

    return redirect('cart:cart_detail')
