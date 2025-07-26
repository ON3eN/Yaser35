from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from cart.models import CartItem  # ⬅️ ضروري لإدارة السلة من قاعدة البيانات

def login_view(request):
    """
    عرض ومعالجة تسجيل الدخول باستخدام اسم المستخدم أو البريد.
    """
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # محاولة تسجيل الدخول باسم المستخدم
        user = authenticate(request, username=username_or_email, password=password)

        # إذا فشل، نحاول تسجيل الدخول بالبريد الإلكتروني
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"مرحباً بك يا {user.first_name or user.username}!")

            # ✅ تحميل السلة من قاعدة البيانات إلى session
            cart_items = []
            for item in CartItem.objects.filter(user=user):
                cart_items.append({
                    'id': item.product.id,
                    'name': item.product.name,
                    'price': float(item.product.price),
                    'quantity': item.quantity,
                    'image_url': item.product.image.url if item.product.image else '',
                })
            request.session['cart_items'] = cart_items

            return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
            return redirect('account:login')

    return render(request, 'account/login.html')


def register_view(request):
    """
    معالجة إنشاء حساب جديد.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        country_code = request.POST.get('country_code', '+966')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "كلمتا المرور غير متطابقتين.")
            return redirect('account:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم مستخدم بالفعل.")
            return redirect('account:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني مستخدم بالفعل.")
            return redirect('account:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        try:
            Profile.objects.create(user=user, phone=f"{country_code}{phone_number}")
        except Exception as e:
            print(f"خطأ في إنشاء الملف الشخصي: {e}")

        messages.success(request, "تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول الآن.")
        return redirect('account:login')

    return render(request, 'account/register.html')


@login_required
def account_settings(request):
    """
    عرض صفحة إعدادات الحساب.
    """
    return render(request, 'account/settings.html')


@login_required
def payment_settings(request):
    """
    عرض صفحة إعدادات الدفع (صيانة حالياً).
    """
    return render(request, 'account/payment_settings.html')
