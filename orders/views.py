import uuid
import logging
from datetime import datetime, date, time, timezone
from django.conf import settings
from django import forms
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

logger = logging.getLogger(__name__)

# Create your views here.
def order_create(request, customer_token):
    """
    Function to display the customer_create.html template
    which will allow new customers to be added.
    """
    order_form = OrderForm(request.POST)
    customer = get_object_or_404(Customer, customer_token=customer_token)
    item = get_object_or_404(Item, id=order_form.cleaned_data['item'].value())
    logger.warning("0")
    logger.warning(request.POST)
    logger.warning("1")
    # logger.warning(order_form)
    logger.warning(customer)
    if request.method == "POST":
        #order = order_form.save(commit=False)
        #invoice = Invoice
        # Order: customer, item , cost_initial, cost_week,
        # start_date,end_date,created_on
        start_date_date = datetime.strptime(order_form.cleaned_data['start_date'].value(), '%Y-%m-%d')
        end_date_date = datetime.strptime(order_form.cleaned_data['end_date'].value(), '%Y-%m-%d')
        logger.warning("1.5")
        order = Order()
        order.item = item
        cost_initial = order_form.cleaned_data['cost_initial'].value()
        cost_week = order_form.cleaned_data['cost_week'].value()
        start_date = start_date_date,
        end_date = end_date_date,
        created_by = request.user,
        logger.warning(order)
        """
        logger.warning(Order(customer = customer,
                    item = item,
                    cost_initial = order_form['cost_initial'].value(),
                    cost_week = order_form['cost_week'].value(),
                    start_date = start_date_date,
                    end_date = end_date_date,
                    created_by = request.user,
                    created_on = datetime.now))
        order = Order(customer = customer,
                    item = item,
                    cost_initial = order_form['cost_initial'].value(),
                    cost_week = order_form['cost_week'].value(),
                    start_date = start_date_date,
                    end_date = end_date_date,
                    created_by = request.user,
                    created_on = datetime.now)
        """
        logger.warning("2")
        logger.warning(order)
        logger.warning(request)
        logger.warning("3")
        #
        invoice = Invoice(order = order,
                            amount_paid = order_form['cost_initial'].value(),
                            note = "First Rental Payment",
                            status = False)
        logger.warning("4")
        logger.warning(invoice)

        if order_form.is_valid():
            logger.warning("5")
            #logger.warning(invoice)
            #logger.warning(order)
            order.save()
            invoice.save()
            
            messages.add_message(
                request, messages.SUCCESS,
                'Order has been saved'
            )
            
            return redirect('customers:customer_order_view', customer_token=order.customer.customer_token, id=order.id)

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