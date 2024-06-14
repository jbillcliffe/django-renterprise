from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import Item
from .forms import ItemForm, ItemTypeForm


# Create your views here.
class ItemList(ListView):
    """
    Class ListView to display the items into a table.
    """
    paginate_by = 9
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        return context


def item_view(request, id):
    """
    Function to view a singular item after being selected.
    """
    # Find a singular Item object. Look in "Item" table in the pk
    # primary key field (auto generated by Django).
    obj = get_object_or_404(Item, pk=id)
    # Render the template item_view and send the found "Item" to it.
    return render(
        request,
        "items/item_view.html",
        {
            "item": obj,
        },
    )


def item_create(request):
    """
    Function to display the item_create.html template
    which will allow new items to be added based on existing
    types.
    """
    item_form = ItemForm(data=request.POST)
    if request.method == "POST":
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.delivery_date = None
            item.collect_date = None
            item.repair_date = None
            item.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New item has been added'
            )
            return redirect('items:item_view', id=item.pk)

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
        item_type_form = ItemTypeForm(request.POST, request.FILES)
        if item_type_form.is_valid():
            item_type = item_type_form.save(commit=False)
            item_type.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New item type has been added'
            )
            return redirect('items:item_list')
    item_type_form = ItemTypeForm()
    return render(
        request,
        "items/item_type_create.html",
        {
            "item_type_form": item_type_form,
        },
    )


def item_status_change(request, id, status):
    item = get_object_or_404(Item, pk=id)
    item.pk = id
    item.status = status
    if status == "4" or status == "Repair" or status == 4:
        item.repair_date = datetime.utcnow()
    else:
        pass
    item.save()
    messages.add_message(
        request, messages.SUCCESS,
        'Item status has been updated'
    )

    return redirect('items:item_view', id=id)
