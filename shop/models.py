from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from users.models import Address



def upload_to_path(instance, filename):
    category_slug = slugify(instance.category.name)
    return f'images/{category_slug}/{filename}'


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


class CartedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username} | {self.quantity} - {self.product.title}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'Accepted for Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} | {self.pk} - {self.status}"


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='invoice/')

    def __str__(self):
        return f"{self.user.username} - {self.order.id}"
