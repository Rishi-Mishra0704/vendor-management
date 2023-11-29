from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import PurchaseOrder
from .serializer import PurchaseOrderSerializer
# Create your views here.


@api_view(['GET'])
def purchase_orders(request):
    purchaseOrders = PurchaseOrder.objects.all()
    serializers = PurchaseOrderSerializer(purchaseOrders, many=True)
    return Response(serializers.data)


@api_view(['POST'])
def purchase_order_create(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, po_id):
    try:
        purchaseOrder = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchaseOrder)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchaseOrder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchaseOrder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

