from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from store.models import Product
from .models import Order

@login_required
def checkout_view(request):
    cart = request.session.get('cart_items', [])

    if not cart:
        messages.error(request, "السلة فارغة")
        return redirect('cart:cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment = request.POST.get('payment')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')

        total_price = 0
        order_details = []

        for item in cart:
            try:
                product = Product.objects.get(id=item['id'])
                quantity = item.get('quantity', 1)
                price = product.price * quantity
                total_price += price

                # إنشاء طلب
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    # ↓↓↓ إذا كانت هذه الحقول موجودة في الموديل Order
                    # full_name=full_name,
                    # phone=phone,
                    # address=address,
                    # payment_method=payment,
                    # latitude=latitude,
                    # longitude=longitude
                )

                order_details.append(f"- {product.name} × {quantity} = {price:.2f} ريال")

            except Product.DoesNotExist:
                continue

        # تفريغ السلة
        request.session['cart_items'] = []

        # رسالة نجاح للمستخدم
        messages.success(request, "تم تأكيد طلبك بنجاح!")

        # إرسال بريد للمستخدم
        send_mail(
            subject="✔️ تم تأكيد طلبك - شقف",
            message=f"""مرحبًا {request.user.username} 👋،

تم استلام طلبك بنجاح ✅

تفاصيل الطلب:
{chr(10).join(order_details)}

📦 المجموع الكلي: {total_price:.2f} ريال
طريقة الدفع: {payment}

📍 العنوان: {address}
📱 الجوال: {phone}

شكرًا لتسوقك معنا 💙
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False
        )

        # إرسال إشعار لصاحب المتجر
        send_mail(
            subject="🛒 طلب جديد من عميل",
            message=f"""📥 طلب جديد من {request.user.username}

📧 البريد: {request.user.email}
📍 الموقع: https://www.google.com/maps?q={latitude},{longitude}

تفاصيل الطلب:
{chr(10).join(order_details)}

📱 الجوال: {phone}
🏠 العنوان: {address}
💳 الدفع: {payment}
💰 الإجمالي: {total_price:.2f} ريال
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )

        return redirect('home')

    return render(request, 'checkout.html')
