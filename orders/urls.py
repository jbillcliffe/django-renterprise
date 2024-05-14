from . import views
from django.urls import path
"""
URLs relating to order navigation (add/edit/"delete")
- delete will always keep a record as it may not want associated
data removed.
- '' = root/items/
- '' is the url for item searching
- 'identifier/' is the url for a single item display
"""

urlpatterns = [
    path('', views.view_orders, name='view_orders'),
]