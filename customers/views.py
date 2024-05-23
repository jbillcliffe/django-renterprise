from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
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
        logger.debug("Attempting to connect to API")
        if customer_form.is_valid():
            logger.debug(customer_form.is_valid())
            logger.debug(customer_form.data)
            customer = customer_form.save(commit=False)
            #customer
            """ 
            customer.first_name = customer_form.first_name
            customer.last_name = customer_form.last_name
            customer.address_line_one = customer_form.address_line_one
            customer.address_line_two = customer_form.address_line_two
            customer.address_line_three = customer_form.address_line_three
            customer.address_line_town = customer_form.address_line_town
            customer.address_line_county = customer_form.address_line_county
            customer.postcode = customer_form.postcode
            """

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
        #else:
            #for error in customer_form.errors:
  

#def customer_search(request):
#    """
#    Function to load the customer search feature
#    """
#    
#    
#    return HttpResponse('Hello Customer Search!')