from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def main_menu(request):
    """
    Function to display the main menu at the root
    of the project
    """
    # return HttpResponse("Hello, Main menu!")
    template_name = "menu/main_menu.html"

    return render(
        request,
        "menu/main_menu.html",
    )