from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'السلة'
        verbose_name_plural = 'السلال'

    def __str__(self):
        return f"سلة {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True)  # مؤقتاً null=True لحل مشكلة الترحيل
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'عنصر في السلة'
        verbose_name_plural = 'عناصر السلة'

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
