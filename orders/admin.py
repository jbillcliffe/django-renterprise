from django.contrib import admin
from .models import Order, OrderNote, Invoice
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    list_display = ('id', 'order_item_name', 'start_date', 'end_date')


@admin.register(OrderNote)
class OrderNoteAdmin(SummernoteModelAdmin):
    list_display = ('order', 'created_on', 'created_by')
    summernote_fields = ('note',)


@admin.register(Invoice)
class InvoiceAdmin(SummernoteModelAdmin):
    list_display = ('order', 'created_on', 'amount_paid', 'status')
    summernote_fields = ('note',)
