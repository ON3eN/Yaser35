from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField("رقم الجوال", max_length=20, blank=True)
    address = models.TextField("العنوان", blank=True)

    def __str__(self):
        return self.user.username

# إرسال إيميل ترحيبي عند إنشاء الحساب
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = "🎉 مرحبًا بك في شقف!"
        message = f"""
مرحبًا {instance.username} 👋،

نشكر لك انضمامك إلى متجر شقف الإلكتروني!

نتمنى لك تجربة تسوق رائعة مليئة بالعروض والمنتجات المميزة.

📦 يمكنك الآن تصفح المنتجات، إضافتها إلى السلة، وتتبع طلباتك بسهولة.

تحياتنا،
فريق شقف ❤️
        """
        send_mail(
            subject=subject,
            message=message,
            from_email='goto6946@gmail.com',
            recipient_list=[instance.email],
            fail_silently=False,
        )
