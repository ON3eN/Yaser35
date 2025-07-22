from django.db import models

class Product(models.Model):
    name = models.CharField("اسم المنتج", max_length=100)
    description = models.TextField("الوصف", blank=True)
    price = models.DecimalField("السعر", max_digits=10, decimal_places=2)
    image = models.ImageField("صورة المنتج", upload_to='product_images/', blank=True, null=True)
    available = models.BooleanField("متوفر؟", default=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)

    def __str__(self):
        return self.name
