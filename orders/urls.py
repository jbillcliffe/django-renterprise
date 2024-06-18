from . import views
from django.urls import path

"""
URLs relating to order navigation
- delete will always keep a record as it may not want associated
data removed.
- '' = root/orders/
"""

app_name = "orders"

urlpatterns = [
    path('',
         views.OrderList.as_view(),
         name='order_list'),
    path('view/<int:id>',
         views.order_view,
         name='order_view'),
    path('<uuid:customer_token>/create/',
         views.order_create,
         name='order_create'),
]
