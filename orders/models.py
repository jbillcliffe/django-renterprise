import uuid
from django.db import models
from django.contrib.auth.models import User
from items.models import Item
from customers.models import Customer

# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="order_customer"
    )
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="order_item"
    )
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_created_by"
    )

class OrderNote(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order"
    )
    note = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="ordernote_created_by"
    )
