from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    # ربط الطلب بالمستخدم والمنتج
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")

    # تفاصيل الطلب
    quantity = models.PositiveIntegerField("الكمية", default=1)
    full_name = models.CharField("الاسم الكامل", max_length=100, null=True, blank=True)
    phone = models.CharField("رقم الجوال", max_length=20, null=True, blank=True)
    address = models.TextField("العنوان", null=True, blank=True)
    latitude = models.FloatField("خط العرض", null=True, blank=True)
    longitude = models.FloatField("خط الطول", null=True, blank=True)
    payment_method = models.CharField("طريقة الدفع", max_length=30, null=True, blank=True)

    # تاريخ الطلب
    ordered_at = models.DateTimeField("تاريخ الطلب", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} × {self.quantity}"

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
