"""
URL configuration for renterprise project.

- Sets the admin panel url and accounts (Django auth)
- "customers" urls in place so the urls start "project.com"/customers/,
url data after this point relates to adding/editing customers.
- "items" urls in place so the urls start "project.com"/items/,
url data after this point relates to adding/editing items.

More URL explainations within each urls.py file.
"""
from django.contrib import admin
from django.urls import path, include
from django.template.loader import get_template

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('customers/', include('customers.urls'), name='customers-urls'),
    path('items/', include('items.urls'), name='items-urls'),
    path('orders/', include('orders.urls'), name='orders-urls'),
    path('', include('menu.urls'), name='menu-urls'),
]