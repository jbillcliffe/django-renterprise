
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Item, ItemType

#import django_tables2 as tables

# Create your views here.

#class SimpleTable(tables.Table):
#    class Meta:
#        model = Simple
#
#class TableView(tables.SingleTableView):
#   table_class = Item
#    queryset = Item.objects.all()
#    template_name = "items/item_search.html"
class ItemList(ListView):
    paginate_by = 9
    model = Item
    #queryset = Item.objects.all()
    #page = request.GET.get('page', 1)
    #paginator = Paginator(queryset, 9)
    #try:
    #    items = paginator.page(page)
    #except PageNotAnInteger:
    #    items = paginator.page(1)
    #except EmptyPage:
     #   items = paginator.page(paginator.num_pages)

    #return render(request, 'items/item_search.html', { 'items': items })
    #template_name = 'items/item_search.html'
    #paginator = Paginator(queryset, 9)

    #paginator.page(1)
    #print(paginator.count)

    #print(paginator.num_pages)

    #print(paginator.page_range)
    
    # paginate_by = 9


# def item_search(request):
#     """
#     function to display the item search feature. Display and paginate
#     all found instances under the search critera (or all can be selected)
#     """
#    template_name = "items/item_search.html"
#    #item_search_form = ItemSearchForm()
#    #paginate_by = 10
#
    #if request.method == "POST":
    #    item_search_form = ItemSearchForm(data=request.POST)
    #    if item_search_form.is_valid():
    #        for field in Entry.objects.all():
    #        queryset = Item.objects.filter(status=1)
    #        post = get_object_or_404(queryset, slug=slug)
    #
    #return render(
    #    request,
    #    "items/item_search.html",
    #    {
    #        "item_search_form":item_search_form,
    #    }
    #)



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