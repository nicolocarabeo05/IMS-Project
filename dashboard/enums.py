from django.db import models


class Category(models.TextChoices):
    STATIONARY = "Stationary", "Stationary"
    ELECTRONICS = "Electronics", "Electronics"
    FOOD = "Food", "Food"


class OrderStatus(models.TextChoices):
    PROCESSING = "Processing", "Processing"
    FOR_DELIVERY = "For Delivery", "For Delivery"
    DELIVERED = "Delivered", "Delivered"
    CANCELLED = "Cancelled", "Cancelled"
