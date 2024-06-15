import uuid
import logging
from django.core.paginator import Paginator
from datetime import datetime, date, time, timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from items.models import Item
from customers.models import Customer

logger = logging.getLogger(__name__)

# Create your models here.
class Order(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']

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

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Order ID : {self.id} - {self.customer.last_name}"

    def order_customer_name(self):
        if self.customer.first_name in self.null_values:
            return f"{self.customer.last_name}"
        else:
            return f"{self.customer.first_name} {self.customer.last_name}"

    def order_item_name(self):
        return f"{self.item.item_type.name}"
        

class OrderNote(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order"
    )
    note = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="ordernote_created_by"
    )

    class Meta:
        ordering = ["created_by"]

    def __str__(self):
        return f"Order Note ID : {self.id}"

    def order_note_full_name(self):
        if self.order.customer.first_name in self.null_values:
            return f"{self.order.customer.last_name}"
        else:
            return f"{self.order.customer.first_name} {self.order.customer.last_name}"

    def created_on_by(self):
        date_to_string = self.created_on.strftime("%d-%m-%Y")
        return f"Created on : {date_to_string}, By : {self.created_by.username}"

    
class Invoice(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']
    
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="invoice_order"
    )
    created_on = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField()
    status = models.BooleanField(default=False)

    # order by item_type name 0-9 then A-Z
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Invoice ID : {self.id}"

    #will send a string of true/false
    def invoice_css_status(self):
        if self.status == True or self.status == "True":
            self = str("paid")
        else :
            self = str("")
        return self
    
    def invoice_customer_name(self):
        if self.order.customer.first_name in self.null_values:
            return f"{self.order.customer.last_name}"
        else:
            return f"{self.order.customer.first_name} {self.order.customer.last_name}"
        