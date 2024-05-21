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
]