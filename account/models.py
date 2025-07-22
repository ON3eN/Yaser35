from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField("رقم الجوال", max_length=20, blank=True)
    address = models.TextField("العنوان", blank=True)

    def __str__(self):
        return self.user.username
