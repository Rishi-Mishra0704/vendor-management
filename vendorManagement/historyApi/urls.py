# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('vendors/<int:vendor_id>/performance/',
         views.vendor_performance, name='vendor_performance'),
]
