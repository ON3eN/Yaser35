from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("الكمية", default=1)
    ordered_at = models.DateTimeField("تاريخ الطلب", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
