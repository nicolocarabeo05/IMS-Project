from django.db import models
from django.contrib.auth.models import User
from .enums import Category, OrderStatus


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=Category.choices, null=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name_plural = "Product"

    def __str__(self):
        return f"{self.name} - {self.category}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING
    )

    class Meta:
        verbose_name_plural = "Order"

    def __str__(self):
        product_name = self.product.name if self.product else "No Product"
        staff_name = self.staff.username if self.staff else "No Staff"

        return f"{product_name} ({self.order_quantity}) - {staff_name}"
