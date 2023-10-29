from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    phone = PhoneNumberField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
