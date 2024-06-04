
from datetime import datetime
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer, CustomerNote
from orders.models import Order
from items.models import Item
from .forms import CustomerForm, CustomerNoteForm
from .urls import *

# Create your views here.
class CustomerList(ListView):
    paginate_by = 9
    model = Customer
    queryset = Customer.objects.exclude(status=2)
    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.
    # This will allow DRY manipulation of the side-bar.html
    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data(**kwargs)
        context['class_var'] = "Customers"
        return context

def customer_view(request, customer_token):
    """
    Function to view a singular customer after being selected.
    """
    template_name = "customers/customer_view.html"
    
    # Find a singular Customer object. Look in "Customer" table in the token
    # field (generated in the customer model using UUID).
    obj = get_object_or_404(Customer, customer_token=customer_token)

    # Render the template customer_view and send the found "Customer" to it.
    return render(
        request,
        "customers/customer_view.html",
        {
            "customer":obj,
            "order_location":"CustomerView",
            "class_var":"Customers",
        },
    )

def customer_create(request):
    """
    Function to display the customer_create.html template
    which will allow new customers to be added.
    """
    customer_form = CustomerForm(request.POST)
    
    if request.method == "POST":
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer has been saved'
            )
            return redirect('customers:customer_view', customer_token=customer.customer_token)

    customer_form = CustomerForm()
    return render(
        request,
        "customers/customer_create.html",
        {
            "customer_form": customer_form,
            "class_var":"Customers",
        },
    )
    
"fix/customer create redirect to customer"
class CustomerNotesList(ListView):
    paginate_by = 9
    model = CustomerNote

    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.
    # This will allow DRY manipulation of the side-bar.html (class_var)

    template_name = "customers/customer_notes_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, customer_token=self.kwargs["customer_token"])
        return CustomerNote.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        context = super(CustomerNotesList, self).get_context_data(**kwargs)
        context['class_var'] = "Customers"
        context['note_list'] = self.get_queryset
        context['order_location'] = "CustomerView"
        context['customer_token_value'] = self.customer.customer_token
        return context

def customer_add_notes(request, customer_token):
    """
    Function to display the customer_add_notes.html template
    which will allow new customer notes to be added.
    """
    if request.method == "POST":
        customer = get_object_or_404(Customer, customer_token=customer_token)
        customer_note_form = CustomerNoteForm(data=request.POST)
        if customer_note_form.is_valid():
            customer_note = customer_note_form.save(commit=False)
            customer_note.customer = customer
            customer_note.created_by = request.user
            customer_note.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer note has been saved'
            )
            return redirect('customers:customer_notes_list', customer_token=customer_token)
    customer_note_form = CustomerNoteForm()
    return render(
        request,
        "customers/customer_add_notes.html",
        {
            "customer_note_form": customer_note_form,
            "order_location":"CustomerView",
            "class_var":"Customers",
        },
    )

def customer_view_notes(request, customer_token, id):
    """
    Function to display the customer_view_notes.html template
    which will allow new authorised users (pre-authorised) to update notes.
    Will also log date and user who did an update.
    https://docs.djangoproject.com/en/5.0/ref/request-response/
    """ 
    # getting initial note value to send to the form
    customer_note_get = get_object_or_404(CustomerNote, pk=id)
    customer_note_text = customer_note_get.note

    if request.method == "POST":
        customer_note_form = CustomerNoteForm(data=request.POST)
        if customer_note_form.is_valid():
            # build note/editname/editdate for records
            newnote = request.POST.get('note', '')
            editname = " By : "+request.user.username+")"
            editdate = " (Edited : "+datetime.utcnow().strftime('%d-%m-%Y')
            fullnote = ''.join([newnote, editdate, editname])
            customer_note_get.pk = id
            customer_note_get.note = fullnote
            customer_note_get.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer note has been updated'
            )
            #return reverse('customer_notes_list', urlconf=None, args=None, kwargs=None, current_app=None)
            return redirect('customers:customer_notes_list', customer_token=customer_token)
    # set initial note in form to be what was previously saved
    customer_note_form = CustomerNoteForm(initial={"note": customer_note_text})
    return render(
        request,
        "customers/customer_view_notes.html",
        {
            "customer_note_form": customer_note_form,
            "order_location":"CustomerView",
            "class_var":"Customers",
        },
    )

class CustomerOrderList(ListView):
    paginate_by = 5
    model = Order

    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.
    # This will allow DRY manipulation of the side-bar.html (class_var)
    #
    # get_context_data now used for different features. Location is assigned differently.
    template_name = "customers/customer_order_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, customer_token=self.kwargs["customer_token"])
        return Order.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        context = super(CustomerOrderList, self).get_context_data(**kwargs)
        context['class_var'] = "Customers"
        context['order_list'] = self.get_queryset
        context['order_location'] = "CustomerOrderListView"
        context['customer_token_value'] = self.customer.customer_token
        return context

def customer_order_view(request, customer_token, id):
    """
    Function to view a singular order after being selected.
    """
    template_name = "customers/order_customer_view.html"
    
    # Find a singular Item object. Look in "Item" table in the pk
    # primary key field (auto generated by Django).
    obj = get_object_or_404(Order, pk=id)
    # Render the template item_view and send the found "Item" to it.
    return render(
        request,
        "customers/customer_order_view.html",
        {
            "order":obj,
            "order_location":"OrderView",
            "class_var":"Customers",
        },
    )
