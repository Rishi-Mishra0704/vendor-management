from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.vendors, name='vendors'),
    path('vendors/create', views.vendor_create, name='vendors_create'),
    path('vendors/<int:vendor_id>/',
         views.vendor_detail, name='vendor_detail'),
]
