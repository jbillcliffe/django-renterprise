from django.db import models
from decimal import Decimal
from cloudinary.models import CloudinaryField

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
    image = CloudinaryField('image', default="placeholder")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default="Category")
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)
    # order by name 0-9 then A-Z
    class Meta:
        ordering = ["name"]
    
    # so the name will replace "ItemType Object" in all instances
    def __str__(self):
        return self.name

        

class Item(models.Model):
    # Best practice for django constants :
    # https://stackoverflow.com/questions/12822847/best-practice-for-python-django-constants
    AVAILABLE = 0
    SCRAPPED = 1
    LOST_STOLEN = 2
    SOLD = 3
    STATUS = (
        (AVAILABLE, 'Available'),
        (SCRAPPED, 'Scrapped'),
        (LOST_STOLEN, 'Lost/Stolen'),
        (SOLD, 'Sold'),
    )

    item_type = models.ForeignKey(
        ItemType, on_delete=models.CASCADE, related_name="item_type"
    )
    item_serial = models.CharField(max_length=200)
    delivery_date = models.DateField(null=True, blank=True)
    collect_date = models.DateField(null=True, blank=True)
    repair_date = models.DateField(null=True, blank=True)
    income = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    status = models.IntegerField(choices=STATUS, default=AVAILABLE)

    # order by item_type name 0-9 then A-Z
    class Meta:
        ordering = ["item_type"]

    # return a formatted string for the name of the item type
    def item_type_name(self):
        return f"{self.item_type.name}"
    
    # return a formatted string for the name of the item type category
    def item_type_category(self):
        return f"{self.item_type.category}"

    # self.status  refers to the variable (eg. AVAILABLE),
    # the index refers to the value this variable hold
    # eg. 'Available'
    def status_str(self):
        return self.STATUS[self.status][1]

    def item_css_status(self):
        self = str(self.STATUS[self.status][1]).replace('/','_').lower()
        return self

    def __str__(self):
        return self.item_type.name