from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from .models import Customer, CustomerNote
from .forms import CustomerForm

# Create your views here.
class CustomerList(ListView):
    paginate_by = 9
    model = Customer
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
    if request.method == "POST":
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.first_name = request.first_name
            customer.last_name = request.last_name
            customer.address_line_one = request.address_line_one
            customer.address_line_two = request.address_line_two
            customer.address_line_three = request.address_line_three
            customer.address_line_town = request.address_line_town
            customer.address_line_county = request.address_line_county
            customer.postcode = request.postcode
            customer.save()

            messages.add_message(
                request, messages.SUCCESS,
                'New item has been added'
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


#def customer_search(request):
#    """
#    Function to load the customer search feature
#    """
#    
#    
#    return HttpResponse('Hello Customer Search!')