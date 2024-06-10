
from datetime import datetime
import logging
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect

from .models import Customer, CustomerNote
from orders.models import Order, OrderNote, Invoice
from orders.forms import OrderNoteForm
from items.models import Item
from .forms import CustomerForm, CustomerNoteForm
from .urls import *

logger = logging.getLogger(__name__)

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
            "customer_token_value":customer_token,
            "full_name":obj.full_name,
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
        },
    )

class CustomerNotesList(ListView):
    paginate_by = 9
    model = CustomerNote

    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.

    template_name = "customers/customer_notes_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, customer_token=self.kwargs["customer_token"])
        return CustomerNote.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        context = super(CustomerNotesList, self).get_context_data(**kwargs)
        context['note_list'] = self.get_queryset
        context['customer_token_value'] = self.customer.customer_token
        context['full_name'] = self.customer.full_name
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
            "customer_token_value": customer_token,
            "full_name": customer.full_name,
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
            "customer_token_value": customer_token,
            "full_name": customer_note_get.customer.full_name,
        },
    )

class CustomerOrderList(ListView):
    paginate_by = 5
    model = Order

    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.
    #
    # get_context_data now used for different features. Location is assigned differently.
    template_name = "customers/customer_order_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, customer_token=self.kwargs["customer_token"])
        return Order.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        context = super(CustomerOrderList, self).get_context_data(**kwargs)
        context['order_list'] = self.get_queryset
        context['customer_token_value'] = self.customer.customer_token
        context['full_name'] = self.customer.full_name
        return context

def customer_order_view(request, customer_token, id):
    """
    Function to view a singular order after being selected.
    """
    template_name = "customers/order_customer_view.html"
    
    # Find a singular Item object. Look in "Item" table in the pk
    # primary key field (auto generated by Django).
    obj = get_object_or_404(Order, pk=id)
    invoice_list = Invoice.objects.filter(order=obj.id).order_by("created_on").values()
    paginate_invoice_list = Paginator(invoice_list, 4)
    #adding pagination to a non-class ListView
    #https://www.geeksforgeeks.org/how-to-add-pagination-in-django-project/
    page_number = request.GET.get('page')
    try:
        # returns the desired page object
        page_obj = paginate_invoice_list.get_page(page_number) 
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginate_invoice_list.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginate_invoice_list.page(paginate_invoice_list.num_pages)
        

    return render(
        request,
        "customers/customer_order_view.html",
        {
            "order": obj,
            "customer_order_id": obj.id,
            "invoice_list": invoice_list,
            "page_obj": page_obj,
            "customer_token_value": customer_token,
            "full_name": obj.customer.full_name,
        },
    )

def invoice_status_change(request, customer_token, order_id,
                        invoice_id, set_invoice):

    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if (set_invoice == "false" or set_invoice == "False"):
        invoice.status = False
    else:
        invoice.status = True
    
    invoice.save()
    messages.add_message(
        request, messages.SUCCESS,
    'Invoice status has been updated'
    )
    return redirect('customers:customer_order_view', 
        customer_token=customer_token,
        id=order_id)

class OrderNotesList(ListView):
    paginate_by = 9
    model = OrderNote

    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.

    template_name = "customers/customer_order_notes_list.html"

    def get_queryset(self):
        self.order = get_object_or_404(Order, id=self.kwargs["order_id"])
        logger.warning(OrderNote.objects.filter(order=self.order))
        return OrderNote.objects.filter(order=self.order)


    def get_context_data(self, **kwargs):
        context = super(OrderNotesList, self).get_context_data(**kwargs)
        context['order_notes_list'] = self.get_queryset
        context['customer_order_id'] = self.order.id
        context['customer_token_value'] = self.order.customer.customer_token
        return context

def add_order_notes(request, customer_token, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order_note_form = OrderNoteForm(request.POST)
        if order_note_form.is_valid():
            order_note = order_note_form.save(commit=False)
            order_note.order = order
            order_note.created_by = request.user
            order_note.save()
        #order,note,created_on,created_on_by
        #logger.warning(order)
        #logger.warning(order_note_form['note'].value())
        #logger.warning(datetime.now)
        #logger.warning(request.user)
        #order_note = OrderNote.objects.create(
        #    order = order,
        #    note = order_note_form['note'].value(),
        #    created_on = datetime.now,
        #    created_by = request.user)
#
        # Validation occurs in JS, so at this point check if the invoice and order have
        # been created and display success message.
       # if order_note.clean() == None:
            messages.add_message(
            request, messages.SUCCESS,
            'Order note has been saved'
            )
            return redirect('customers:order_notes_list', customer_token=customer_token, order_id=order.id)
       
    order_note_form = OrderNoteForm()

    return render(
        request,
        "customers/customer_add_order_notes.html",
        {
            "order_note_form": order_note_form,
            "customer_token_value": customer_token,
            "customer_order_id": order_id,
        },
    )

def order_view_notes(request, customer_token, order_id, id):
    """
    Function to display the customer_view_notes.html template
    which will allow new authorised users (pre-authorised) to update notes.
    Will also log date and user who did an update.
    https://docs.djangoproject.com/en/5.0/ref/request-response/
    """ 
    # getting initial note value to send to the form
    order_note_get = get_object_or_404(OrderNote, pk=id)
    order_note_text = order_note_get.note

    if request.method == "POST":
        order_note_form = OrderNoteForm(data=request.POST)
        if order_note_form.is_valid():
            # build note/editname/editdate for records
            newnote = request.POST.get('note', '')
            editname = " By : "+request.user.username+")"
            editdate = " (Edited : "+datetime.utcnow().strftime('%d-%m-%Y')
            fullnote = ''.join([newnote, editdate, editname])
            order_note_get.pk = id
            order_note_get.note = fullnote
            order_note_get.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Order note has been updated'
            )
            #return reverse('customer_notes_list', urlconf=None, args=None, kwargs=None, current_app=None)
            return redirect('customers:order_notes_list', customer_token=customer_token, order_id=order_id)
    # set initial note in form to be what was previously saved
    order_note_form = OrderNoteForm(initial={"note": order_note_text})
    return render(
        request,
        "customers/customer_view_order_notes.html",
        {
            "order_note_form": order_note_form,
            "customer_token_value": customer_token,
            "customer_order_id":order_id
        },
    )