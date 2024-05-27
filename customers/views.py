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

def customer_notes(request, customer_token):

    template_name = "customers/customer_notes.html"

    get_customer = get_object_or_404(Customer, customer_token=customer_token)
    #customer_notes = Custome rNotes.get_customer.all().order_by("-created_on")
    customer_notes = CustomerNote.objects.filter(customer=get_customer)
   # notes_count = customer_notes.count()

    return render (
        request,
        "customers/customer_notes.html",
        {
            "class_var":"Customers",
        },
    )

def view_customer_note(request):
    print("Hello note")
#def customer_search(request):
#    """
#    Function to load the customer search feature
#    """
#    
#    
#    return HttpResponse('Hello Customer Search!')