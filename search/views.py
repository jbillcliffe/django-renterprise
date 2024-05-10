from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def search_data(request):
    """
    Function to render the searching page.
    Has multiple search filters.
    """
    return HttpResponse('Hello Search feature')