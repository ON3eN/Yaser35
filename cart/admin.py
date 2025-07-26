from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'added_at')
    can_delete = False
    verbose_name = "عنصر في السلة"
    verbose_name_plural = "عناصر السلة"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'product', 'quantity', 'added_at')
    search_fields = ('cart__user__username', 'product__name')
    list_filter = ('added_at', 'product')
    ordering = ('-added_at',)

    def get_username(self, obj):
        return obj.cart.user.username
    get_username.short_description = 'اسم المستخدم'
