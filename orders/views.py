import uuid
from datetime import datetime
from django.conf import settings
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
def order_create(request, customer_token):
    """
    Function to display the customer_create.html template
    which will allow new customers to be added.
    """
    order_form = OrderForm(request.POST)
    customer = get_object_or_404(Customer, customer_token=customer_token)

    if request.method == "POST":
        # Order: customer, item , cost_initial, cost_week,
        # start_date,end_date,created_on
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = customer
            order.created_by = request.user
            order.save()
            # Invoice: order, created_on, amount_paid,
            # note, status
            invoice = model.Invoice
            invoice.order = order
            invoice.amount_paid = order.cost_initial
            invoice.note = "Initial hire cost"
            invoice.status = False
            invoice.save()

            messages.add_message(
                request, messages.SUCCESS,
                'Order has been saved'
            )

            #return redirect('orders:order_view', customer_token=customer_token, id=order.id)

    order_form = OrderForm()

    return render(
        request,
        "orders/order_create.html",
        {
            "order_form": order_form,
            "class_var":"Orders",
        },
    )

class OrderList(ListView):
    paginate_by = 9
    model = Order
    # needs to set the class var to Customers if this is 
    #from the customer and not the general order list.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_var'] = 'Orders'
        return context

def order_view(request, id):
    """
    Function to view a singular order after being selected.
    """
    template_name = "orders/order_view.html"
    
    # Find a singular Item object. Look in "Item" table in the pk
    # primary key field (auto generated by Django).
    obj = get_object_or_404(Item, pk=id)
    # Render the template item_view and send the found "Item" to it.
    return render(
        request,
        "orders/order_view.html",
        {
            "item":obj,
            "class_var":"Items",
        },
    )