from django.db import models
from django.db.models import Model

# Create your models here.

class Customer(Model):
    unique_id = models.UUIDField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    postcode = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
