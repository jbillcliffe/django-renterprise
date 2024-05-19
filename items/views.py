from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Item, ItemType

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

def item_view(request, id):
    """
    function to display the item search feature
    """
    template_name = "items/item_view.html"

    obj = get_object_or_404(Item, pk=id)


    return render(
        request,
        "items/item_view.html",
        {
            "item":obj,
        },
    )