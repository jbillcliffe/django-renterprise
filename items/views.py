from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def get_items(request):
    """
    function to display the full listing of items
    available to hire.
    """
    return HttpResponse('Hello Items.')