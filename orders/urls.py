from . import views
from django.urls import path
"""
URLs relating to order navigation (add/edit/"delete")
- delete will always keep a record as it may not want associated
data removed.
- '' = root/items/
- '' is the url for item searching
- 'identifier/' is the url for a single item display
"""

app_name = "orders"

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('view/<int:id>',
        views.order_view, name='order_view'),
    path('<uuid:customer_token>/create/',
        views.order_create, name='order_create'),
    path('<uuid:customer_token>/invoices/',
        views.OrderInvoiceList.as_view(), name='order_invoice'),
]