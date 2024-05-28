from django.contrib import admin
from .models import Customer, CustomerNote
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(SummernoteModelAdmin):
    list_display = ('id', 'full_name', 'postcode')

@admin.register(CustomerNote)
class CustomerNoteAdmin(SummernoteModelAdmin):
    list_display = ('full_name', 'created_on', 'created_by')
    summernote_fields = ('note',)