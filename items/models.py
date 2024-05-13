from django.db import models
from decimal import Decimal

"""
Models for ItemType and Item.
-- ItemType
- DecimalField was decided due to being able to set a max number of decimals.
- If less is inputted, the form will convert to 2 decimals before saving.
-- Item --
- DateFields are nullable, if null it frees up the item for booking

- Income field same as ItemType reasoning for DecimalField.
"""

# Create your models here.
class ItemType(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)

class Item(models.Model):
    item_type = models.ForeignKey(
        ItemType, on_delete=models.CASCADE, related_name="item_type"
    )
    item_serial = models.CharField(max_length=200)
    delivery_date = models.DateField(null=True, blank=True)
    collect_date = models.DateField(null=True, blank=True)
    repair_date = models.DateField(null=True, blank=True)
    income = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def item_type_name(self):
        return f"{self.item_type.name}"

    def item_type_category(self):
        return f"{self.item_type.category}"