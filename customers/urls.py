from . import views
from django.urls import path

"""
URLs for customer navigation.
- '' = root/customers/
- '' is the url for customer searching
- 'customer_id/' is the url for a customer's page
- 'customer_id/order_id' is the url of a single order for a customer
"""

app_name = "customers"

urlpatterns = [
    path('', views.CustomerList.as_view(), name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<uuid:customer_token>/', views.customer_view, name='customer_view'),
    path('<uuid:customer_token>/customer_notes_list/', views.CustomerNotesList.as_view(), name='customer_notes_list'),
    path('<uuid:customer_token>/customer_notes_list/<int:id>', views.customer_view_notes, name='customer_view_notes'),
    path('<uuid:customer_token>/customer_notes_list/create/', views.customer_add_notes, name='customer_add_notes'),
]