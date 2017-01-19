from django.contrib import admin
from .models import Cart, Product, CartItem, ProductCategory

class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductCategory)
admin.site.register(CartItem)
