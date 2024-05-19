from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def item_search(request):
    """
    function to display the item search feature
    """
    template_name = "items/item_search.html"

    return render(
        request,
        "items/item_search.html",
    )