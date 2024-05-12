from django.contrib import admin
from .models import Item, ItemType
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(ItemType)
admin.site.register(Item)