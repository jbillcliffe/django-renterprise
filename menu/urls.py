
from . import views
from django.urls import path

"""
URLs relating to menu navigation
- Contains URLs for the buttons on the main menu to navigate
the rest of the program
- This is the root page for the project and "menu" URLs ie.
www.website.com/menu does not exist. To get to the menu, you
navigate to www.website.com
"""
app_name = "menu"
urlpatterns = [
    path('',
         views.main_menu,
         name='menu'),
]
