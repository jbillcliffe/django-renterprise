from django.shortcuts import render


# Create your views here.
def main_menu(request):
    """
    Function to display the main menu at the root
    of the project. Render a template, nothing more.
    """
    return render(
        request,
        "menu/main_menu.html",
    )
