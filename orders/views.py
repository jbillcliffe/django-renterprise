from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main_menu(request):
    """
    Function to display the main menu at the root
    of the project
    """
    return HttpResponse("Hello, Orders!")