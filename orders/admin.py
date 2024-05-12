from django.contrib import admin
from .models import Order, OrderNote, Invoice

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderNote)
admin.site.register(Invoice)