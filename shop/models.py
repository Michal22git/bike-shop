from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum


def upload_to_path(instance, filename):
    category_slug = slugify(instance.category.name)
    return f'static/images/{category_slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-list', args=[self.name.lower()])

    class Meta:
        verbose_name_plural = 'Category'


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Product'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

    def calculate_total(self):
        carted_items = CartedItem.objects.filter(cart=self)
        self.total_items = carted_items.aggregate(Sum('quantity'))['quantity__sum']
        self.total_price = sum(item.product.price * item.quantity for item in carted_items)
        self.save()


class CartedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username} | {self.quantity} - {self.product.title}"
