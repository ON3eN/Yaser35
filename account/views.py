from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from cart.models import Cart, CartItem  # ✅ تم استيراد Cart لتحديث تحميل السلة

def login_view(request):
    """
    تسجيل الدخول باستخدام اسم المستخدم أو البريد الإلكتروني.
    يعيد التوجيه إلى الصفحة السابقة إن وُجدت، أو إلى الصفحة الرئيسية.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            # ✅ تحميل سلة المستخدم الحالية من قاعدة البيانات إلى session
            cart, created = Cart.objects.get_or_create(user=user)
            cart_items = []
            for item in cart.items.all():  # باستخدام related_name='items' في CartItem
                cart_items.append({
                    'id': item.product.id,
                    'name': item.product.name,
                    'price': float(item.product.price),
                    'quantity': item.quantity,
                    'image_url': item.product.image.url if item.product.image else '',
                })
            request.session['cart_items'] = cart_items

            return redirect(next_url)
        else:
            # إعادة التوجيه لنفس الصفحة بدون رسائل
            return redirect(f"{request.path}?next={next_url}")

    return render(request, 'account/login.html', {'next': next_url})


def register_view(request):
    """
    إنشاء حساب جديد.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        country_code = request.POST.get('country_code', '+966')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return redirect('account:register')

        if User.objects.filter(username=username).exists():
            return redirect('account:register')

        if User.objects.filter(email=email).exists():
            return redirect('account:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        try:
            Profile.objects.create(user=user, phone=f"{country_code}{phone_number}")
        except Exception as e:
            print(f"خطأ في إنشاء الملف الشخصي: {e}")

        return redirect('account:login')

    return render(request, 'account/register.html')


@login_required
def account_settings(request):
    return render(request, 'account/settings.html')


@login_required
def payment_settings(request):
    return render(request, 'account/payment_settings.html')
