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
    # url for customer search
    #path('', views.customer_search, name='customer_list'),
    path('', views.CustomerList.as_view(), name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('<uuid:customer_token>/', views.customer_view, name='customer_view'),
    path('<uuid:customer_token>/customer_notes/', views.customer_notes, name='customer_notes'),
    path('<uuid:customer_token>/customer_notes/<int:pk>', views.view_customer_note, name='view_customer_note'),
    #path('<uuid:customer_token>/notes/create/', views.customer_add_notes, name='customer_add_notes'),
]