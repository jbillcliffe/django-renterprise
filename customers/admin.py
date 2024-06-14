from django.contrib import admin
from .models import Customer, CustomerNote
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(SummernoteModelAdmin):
    """
    assign fields to show in the table of customers in the admin
    back end.
    """
    list_display = ('id', 'full_name', 'postcode')


@admin.register(CustomerNote)
class CustomerNoteAdmin(SummernoteModelAdmin):
    """
    assign fields to show in the table of customer notes in the admin
    back end.
    """
    list_display = ('full_name', 'created_on', 'created_by')
    summernote_fields = ('note',)
