from django.contrib import admin
from .models import Category, Product, Cart, CartedItem, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartedItem)
admin.site.register(Order)

