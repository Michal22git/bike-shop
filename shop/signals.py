import os

from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Product, CartedItem, Order


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


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        order = instance
        subject = 'Order Confirmation'
        template_name = 'email/order_confirmation.html'


        context = {
            'order': order,
        }

        html_content = render_to_string(template_name, context)

        send_mail(
            subject,
            '',
            '',
            [order.user.email],
            html_message=html_content,
            fail_silently=False,
        )
