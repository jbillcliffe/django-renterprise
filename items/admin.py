from django.contrib import admin
from .models import Item, ItemType
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(ItemType)
class ItemTypeAdmin(SummernoteModelAdmin):
    list_display = ('name',)


@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):
    list_display = ('item_type_name', 'item_type_category', 'item_serial')
