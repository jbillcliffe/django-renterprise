import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    customer_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    postcode = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)

class CustomerNote(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    note = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_by"
    )

