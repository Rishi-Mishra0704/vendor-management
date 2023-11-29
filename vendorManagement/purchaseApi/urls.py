from django.urls import path

from . import views

urlpatterns = [
    path('purchase_orders/', views.purchase_orders),
    path('purchase_orders/create/', views.purchase_order_create),
    path('purchase_orders/<int:po_id>/', views.purchase_order_detail),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order),
]