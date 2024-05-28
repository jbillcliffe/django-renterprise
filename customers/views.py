from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from .models import Customer, CustomerNote
from .forms import CustomerForm
import logging

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

    customer_form = CustomerForm()
    return render(
        request,
        "customers/customer_create.html",
        {
            "customer_form": customer_form,
            "class_var":"Customers",
        },
    )

class CustomerNotesList(ListView):
    paginate_by = 9
    model = CustomerNote
    #get_customer = get_object_or_404(Customer, customer_token=customer_token)
    #queryset = CustomerNote.objects.filter(customer__customer_token=self.kwargs.get('customer_token'))
    # https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template
    # Override original get_context_data to allow sending of the application area.
    # This will allow DRY manipulation of the side-bar.html

    template_name = "customers/customer_notes_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, customer_token=self.kwargs["customer_token"])
        return CustomerNote.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        context = super(CustomerNotesList, self).get_context_data(**kwargs)
        context['class_var'] = "Customers"
        context['note_list'] = self.get_queryset
        return context

def view_customer_note(request, customer_token, id):
    print("Hello note")

def customer_add_notes(request):
    """
    Function to display the customer_add_notes.html template
    which will allow new customer notes to be added.
    """
    customer_note_form = CustomerNoteForm(request.POST)
    
    if request.method == "POST":
        if customer_note_form.is_valid():
            customer_note = customer_note_form.save(commit=False)
            customer_note.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer note has been saved'
            )

    customer_note_form = CustomerNoteForm()
    return render(
        request,
        "customers/customer_add_notes.html",
        {
            "customer_note_form": customer_note_form,
            "class_var":"Customers",
        },
    )