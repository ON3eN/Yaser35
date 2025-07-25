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

                # حفظ الطلب
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    # أضف المزيد من الحقول إذا لزم الأمر
                )

                order_details.append(f"• {product.name} × {quantity} = {price:.2f} ريال")

            except Product.DoesNotExist:
                continue

        # تفريغ السلة
        request.session['cart_items'] = []

        # إشعار المستخدم
        messages.success(request, "تم تأكيد طلبك بنجاح!")

        # --- رسالة للمستخدم ---
        user_message = f"""
مرحبًا {request.user.username} 👋،

تم استلام طلبك بنجاح في متجر شقف ✅

🔹 تفاصيل الطلب:
{chr(10).join(order_details)}

💰 المجموع الكلي: {total_price:.2f} ريال
💳 طريقة الدفع: {payment}

📍 عنوان التوصيل: {address}
📱 رقم الجوال: {phone}

📦 سيتم تجهيز الطلب وإرساله إليك بأقرب وقت ممكن.

شكراً لاختيارك شقف! 💙
"""

        send_mail(
            subject="✔️ تم تأكيد طلبك - شقف",
            message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False
        )

        # --- رسالة لصاحب المتجر بشكل منسق ---
        admin_message = f"""
🛍️ طلب جديد من {request.user.username}

📧 البريد الإلكتروني:
{request.user.email}

📱 رقم الجوال:
{phone}

🏠 عنوان التوصيل:
{address}

📍 رابط الموقع:
https://www.google.com/maps?q={latitude},{longitude}

📦 تفاصيل الطلب:
{chr(10).join(order_details)}

💳 طريقة الدفع:
{payment}

💰 المجموع الكلي:
{total_price:.2f} ريال
"""

        send_mail(
            subject="📬 طلب جديد - إشعار من شقف",
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )

        return redirect('home')

    return render(request, 'checkout.html')
