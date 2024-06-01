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
from django.views.generic.base import TemplateView
from django.conf import settings

import os
from menu import views

paginate_file = os.path.join(settings.TEMPLATES_DIR, 'paginate.html')
urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('customers/', include('customers.urls'), name='customers-urls'),
    path('items/', include('items.urls'), name='items-urls'),
    path('orders/', include('orders.urls'), name='orders-urls'),
    path('', include('menu.urls'), name='menu-urls'),
    path('templates/paginate/', TemplateView.as_view(template_name=paginate_file), name="paginate_template"),
]

#dir = os.path.join(BASE_DIR, 'templates')
#file_list = os.listdir(dir)
#for file in file_list:
#    path_url = file.replace('.html', '/')
#    name = file.replace('.html', '')
#    path(path_url, 
#    urlpatterns.append(route)