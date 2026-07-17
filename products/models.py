from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=100, default="General")
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
class OrderHistory(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Out of Stock", "Out of Stock"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    delivery_name = models.CharField(max_length=100, default="")
    delivery_mobile = models.CharField(max_length=15, default="")
    delivery_house = models.CharField(max_length=200, default="")
    delivery_street = models.CharField(max_length=200, default="")
    delivery_city = models.CharField(max_length=100, default="")
    delivery_state = models.CharField(max_length=100, default="")
    delivery_pincode = models.CharField(max_length=10, default="")

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    cancel_reason = models.TextField(blank=True, default="")

    def __str__(self):
        return self.product_name

    def __str__(self):
        return self.product_name
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.product.name
class Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)

    house_no = models.CharField(max_length=100)
    street = models.CharField(max_length=200)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=6)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"