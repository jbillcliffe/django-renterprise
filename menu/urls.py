from . import views
from django.urls import path
from django.http import HttpRequest

"""
URLs relating to menu navigation
- Only contains the '' path.
- This is the root for the project and "menu" is not in the

- app_name - THIS REGISTERS THE NAMESPACE FOR URLS
URL. 
"""
app_name = "menu"
urlpatterns = [
    path('', views.main_menu, name='menu'),
]