import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    CURRENT = 0
    DECEASED = 1
    ARCHIVED = 2
    STATUS = (
        (CURRENT, 'Current'),
        (DECEASED, 'Deceased'),
        (ARCHIVED, 'Archived'),
    )

    customer_token = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    postcode = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=CURRENT)

    # order by last_name then first_name 
    # (last name more common for searches)
    class Meta:
        ordering = ["last_name", "first_name"]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class CustomerNote(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    note = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_by"
    )

    def full_name(self):
        return f"{self.customer.first_name} {self.customer.last_name}"