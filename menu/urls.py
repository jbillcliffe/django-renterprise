from . import views
from django.urls import path

"""
URLs relating to menu navigation
- Only contains the '' path.
- This is the root for the project and "menu" is not in the
URL. 
"""

urlpatterns = [
    path('', views.main_menu, name='menu'),
]