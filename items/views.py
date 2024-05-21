from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from .models import Item, ItemType
from .forms import ItemForm, ItemTypeForm

# Create your views here.
class ItemList(ListView):
    paginate_by = 9
    model = Item
    
def item_view(request, id):
    """
    Function to view a singular item after being selected.
    """
    template_name = "items/item_view.html"
    
    # Find a singular Item object. Look in "Item" table in the pk
    # primary key field (auto generated by Django).
    obj = get_object_or_404(Item, pk=id)
    # Render the template item view and send the found "Item" to it.
    return render(
        request,
        "items/item_view.html",
        {
            "item":obj,
        },
    )

def item_create(request):
    """
    Function to display the item_create.html template
    which will allow new items to be added based on existing
    types.
    """
    if request.method == "POST":
        item_form = ItemForm(data=request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.item_type = request.item_type
            item.item_serial = request.item_serial
            item.delivery_date = null
            item.collect_date = null
            item.repair_date = null
            item.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New item has been added'
            )
    item_form = ItemForm()
    return render(
        request,
        "items/item_create.html",
        {
            "item_form": item_form,
            
        },
    )

def item_type_create(request):
    """
    Function to display the item_type_create.html template
    which will allow new item types to be added based on existing
    types.
    """
    if request.method == "POST":
        item_type_form = ItemTypeForm(data=request.POST)
        if item_type_form.is_valid():
            item_type = item_type_form.save(commit=False)
            item_type.name = request.name
            item_type.category = request.category
            item_type.cost_initial = request.cost_initial
            item_type.cost_week = request.cost_week
            item_type.image = request.image
            item_type.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New item type has been added'
            )
    item_type_form = ItemTypeForm()
    return render(
        request,
        "items/item_type_create.html",
        {
            "item_type_form": item_type_form,
        },
    )



    