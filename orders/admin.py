from django.contrib import admin
from .models import Order, OrderNote, Invoice
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderNote)
# admin.site.register(Invoice)

@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    list_display = ('id', 'order_item_name', 'start_date', 'end_date')

@admin.register(OrderNote)
class OrderNoteAdmin(SummernoteModelAdmin):
    list_display = ('order_note_full_name', 'created_on', 'created_by')
    summernote_fields = ('note',)