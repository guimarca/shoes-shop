import uuid

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price})"


class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders",
    )
    shipped = models.BooleanField(default=False)

    @property
    def total_amount(self):
        return sum(pr.total_amount() for pr in list(self.order_products.all()))


class OrderLine(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_lines",
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products",
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    def total_amount(self):
        return self.quantity * self.product.price
