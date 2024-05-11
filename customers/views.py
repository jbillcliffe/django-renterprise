from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def customer_search(request):
    """
    Function to load the customer search feature
    """
    
    
    return HttpResponse('Hello Customer Search!')