import csv
import os
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.db import models
from django.template.loader import render_to_string
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
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    shipped = models.BooleanField(default=False)

    @property
    def total_amount(self):
        return sum(ord_pr.total_amount for ord_pr in list(self.order_products.all()))

    def to_html(self):
        return render_to_string(
            "order_summary.html",
            {
                "order": self,
                "order_products": list(self.order_products.all()),
                "now": datetime.now(),
            },
        )

    def to_csv_file(self):
        with open(f"order_files/order_{self.id}.csv", "w") as order_file:
            order_writer = csv.writer(order_file, delimiter=",", quotechar='"')
            order_writer.writerow(("id", "name", "price", "quantity", "total amount"))
            for ord_pr in list(self.order_products.all()):
                order_writer.writerow(
                    (
                        ord_pr.product.id,
                        ord_pr.product.name,
                        ord_pr.product.price,
                        ord_pr.quantity,
                        ord_pr.total_amount,
                    )
                )
        return order_file.name

    def send_email(self):
        csv_file = self.to_csv_file()
        email = EmailMessage(
            subject=f"Order: {self.id}",
            body=self.to_html(),
            to=[self.customer.email]
        )
        email.content_subtype = 'html'
        email.attach_file(csv_file)
        email.send()
        #   os.remove(csv_file)

    def ship(self):
        self.send_email()
        self.shipped = True
        self.save()


class OrderLine(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_lines",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_products",
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def total_amount(self):
        return self.quantity * self.product.price
