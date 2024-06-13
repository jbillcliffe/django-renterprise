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
    path('<uuid:customer_token>/status_change/<int:status>', 
        views.customer_status_change, name='customer_status_change'),
    path('<uuid:customer_token>/customer_notes_list/', 
        views.CustomerNotesList.as_view(), name='customer_notes_list'),
    path('<uuid:customer_token>/customer_notes_list/<int:id>/',
        views.customer_view_notes, name='customer_view_notes'),
    path('<uuid:customer_token>/customer_notes_list/create/',
        views.customer_add_notes, name='customer_add_notes'),
    path('<uuid:customer_token>/orders/',
        views.CustomerOrderList.as_view(),
        name='customer_order_list'),
    path('<uuid:customer_token>/orders/<int:order_id>',
        views.customer_order_view,
        name='customer_order_view'),
    path('<uuid:customer_token>/orders/<int:order_id>/order_notes_list/',
        views.OrderNotesList.as_view(), name='order_notes_list'),
    path('<uuid:customer_token>/orders/<int:order_id>/order_notes_list/<int:id>',
        views.order_view_notes, name='order_view_notes'),
    path('<uuid:customer_token>/orders/<int:order_id>/order_notes_list/create/',
        views.add_order_notes, name='add_order_notes'),
    path('<uuid:customer_token>/orders/<int:order_id>/invoice_status/<int:invoice_id>/<str:set_invoice>',
        views.invoice_status_change, name='invoice_status_change'),
    path('<uuid:customer_token>/orders/<int:order_id>/invoice_create/<str:amount_paid>/<str:note>/',
        views.invoice_create, name='invoice_create'),
]