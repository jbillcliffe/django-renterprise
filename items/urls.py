from . import views
from django.urls import path

"""
URLs relating to item navigation (add/edit/"delete")
- delete will always keep a record as it may not want associated
data removed.
- '' = root/items/
- '' is the url for item searching
- 'identifier/' is the url for a single item display
"""

app_name = "items"

urlpatterns = [
    path('', views.ItemList.as_view(), name='item_list'),
    path('create/', views.item_create, name='item_create'),
    path('create/item_type/', views.item_type_create, name='item_type_create'),
    path('<int:id>/', views.item_view, name='item_view'),
    path('<int:id>/status_change/<int:status>',
         views.item_status_change, name='item_status_change'),
]