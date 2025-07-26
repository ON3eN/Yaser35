from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import CartItem

# ✅ عرض السلة
def cart_view(request):
    cart_items = []

    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        for item in items:
            cart_items.append({
                'id': item.product.id,
                'name': item.product.name,
                'price': float(item.product.price),
                'quantity': item.quantity,
                'image_url': item.product.image.url if item.product.image else '',
            })
    else:
        cart_items = request.session.get('cart_items', [])

    discount = request.session.get('discount', 0)
    for item in cart_items:
        item['quantity'] = item.get('quantity', 1)
        item['subtotal'] = round(item['price'] * item['quantity'], 2)

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

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    else:
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
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))

# ✅ إضافة باستخدام Ajax
@require_POST
def ajax_add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        count = CartItem.objects.filter(user=request.user).count()
    else:
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
        count = sum(item['quantity'] for item in cart_items)

    return JsonResponse({
        'message': f"✅ تمت إضافة {product.name} إلى السلة 🛒",
        'cartCount': count
    })

# ✅ زيادة الكمية
def increase_quantity(request, product_id):
    if request.user.is_authenticated:
        item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if item:
            item.quantity += 1
            item.save()
    else:
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            if item['id'] == product_id:
                item['quantity'] += 1
                break
        request.session['cart_items'] = cart_items

    return redirect('cart:cart')

# ✅ تقليل الكمية
def decrease_quantity(request, product_id):
    if request.user.is_authenticated:
        item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                messages.warning(request, "📌 إذا كنت تريد حذف المنتج، اضغط على علامة الحذف الحمراء.")
    else:
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            if item['id'] == product_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    messages.warning(request, "📌 إذا كنت تريد حذف المنتج، اضغط على علامة الحذف الحمراء.")
                break
        request.session['cart_items'] = cart_items

    return redirect('cart:cart')

# ✅ إزالة منتج
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    else:
        cart_items = request.session.get('cart_items', [])
        cart_items = [item for item in cart_items if item['id'] != product_id]
        request.session['cart_items'] = cart_items

    messages.info(request, "🗑️ تمت إزالة المنتج من السلة")
    return redirect('cart:cart')

# ✅ تفريغ السلة
def clear_cart(request):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    request.session['cart_items'] = []
    request.session['discount'] = 0
    messages.info(request, "🧺 تم تفريغ السلة بنجاح")
    return redirect('cart:cart')

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
    return redirect('cart:cart')
