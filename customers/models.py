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
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    address_line_one = models.CharField(max_length=200)
    # sometimes people only have a first line before 
    # town is the next entry
    address_line_two = models.CharField(max_length=200, null=True, blank=True)
    address_line_three = models.CharField(max_length=200, null=True, blank=True)
    address_line_town = models.CharField(max_length=200)
    address_line_county = models.CharField(max_length=200)
    # longest UK postcode would be 8 characters including a space
    postcode = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=CURRENT)

    # order by last_name then first_name 
    # (last name more common for searches)
    class Meta:
        ordering = ["last_name", "first_name"]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def status_str(self):
        return self.STATUS[self.status][1]

    def customer_css_status(self):
        self = str(self.STATUS[self.status][1]).lower()
        return self

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