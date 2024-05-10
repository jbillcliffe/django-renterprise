from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_menu, name='menu'),
]