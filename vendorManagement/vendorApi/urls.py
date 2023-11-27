from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.vendors, name='vendors'),
    path('vendors/create', views.vendor_create, name='vendors'),
    path('vendors/<int:vendor_id>/',
         views.vendor_detail, name='vendor_detail'),
    path('vendors/<int:vendor_id>/performance',
            views.vendor_performance, name='vendor_performance'),
]
