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

def customer_view(request, customer_token):
    """
    Function to view a singular customer after being selected.
    """
    template_name = "customers/customer_view.html"
    
    # Find a singular Customer object. Look in "Customer" table in the token
    # field (generated in the customer model using UUID).
    obj = get_object_or_404(Customer, customer_token=customer_token)
    # Render the template customer_view and send the found "Customer" to it.
    return render_to_response(
        request,
        "customers/customer_view.html",
        {
            "customer":obj,
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
            customer.address = request.address
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
            
        },
    )


#def customer_search(request):
#    """
#    Function to load the customer search feature
#    """
#    
#    
#    return HttpResponse('Hello Customer Search!')