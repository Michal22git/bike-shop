import os
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Product, CartedItem


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_save, sender=CartedItem)
@receiver(post_delete, sender=CartedItem)
def update_cart_totals(sender, instance, **kwargs):
    cart = instance.cart
    total_items = cart.carteditem_set.aggregate(Sum('quantity'))['quantity__sum']
    total_price = sum(item.product.price * item.quantity for item in cart.carteditem_set.all())
    cart.total_items = total_items or 0
    cart.total_price = total_price or 0
    cart.save()
