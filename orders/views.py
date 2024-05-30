from datetime import datetime
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect
from customers.models import Customer
from items.models import Item
from .models import Order, OrderNote, Invoice
from .forms import OrderForm
from .urls import *

# Create your views here.
"""
def view_orders(request):
    return HttpResponse("Hello, Orders!")
"""

def order_create(request, customer_token):
    """
    Function to display the customer_create.html template
    which will allow new customers to be added.
    """
    order_form = OrderForm(request.POST)
    customer = get_object_or_404(Customer, customer_token=customer_token)

    if request.method == "POST":
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = customer
            order.created_by = request.user
            order.save()
            #item = request.POST.get('item', '')
            #item.delivery_date = order.start_date
            #item.collect_date = order.end_date
            messages.add_message(
                request, messages.SUCCESS,
                'Order has been saved'
            )
            #return redirect('orders:order_view', customer_token=customer_token,order_id=order.pk)

    order_form = OrderForm()
    return render(
        request,
        "orders/order_create.html",
        {
            "order_form": order_form,
            "class_var":"Orders",
        },
    )