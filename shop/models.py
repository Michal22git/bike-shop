from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
