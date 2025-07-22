from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile  # إذا كنت تستخدم موديل Profile

def login_view(request):
    """
    عرض ومعالجة تسجيل الدخول.
    """
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # محاولة تسجيل الدخول باستخدام اسم المستخدم
        user = authenticate(request, username=username_or_email, password=password)

        # إذا لم ينجح، نحاول بالبريد الإلكتروني
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"مرحباً بك يا {user.username}!")
            return redirect('home')  # تحويل للصفحة الرئيسية
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")
            return redirect('account:login')

    return render(request, 'account/login.html')


def register_view(request):
    """
    معالجة تسجيل حساب جديد من قبل العميل.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "كلمتا المرور غير متطابقتين")
            return redirect('account:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم مستخدم بالفعل")
            return redirect('account:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني مستخدم بالفعل")
            return redirect('account:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # إنشاء ملف شخصي مرتبط بالمستخدم (إذا كنت تستخدم موديل Profile)
        try:
            Profile.objects.create(user=user, phone=phone)
        except:
            pass  # تجاهل إذا لم يوجد موديل Profile

        messages.success(request, "تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول الآن.")
        return redirect('account:login')

    return render(request, 'account/register.html')
