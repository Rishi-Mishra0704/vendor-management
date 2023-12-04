from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from .models import PurchaseOrder
from .serializer import PurchaseOrderSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_orders(request):
    purchaseOrders = PurchaseOrder.objects.all()
    serializers = PurchaseOrderSerializer(purchaseOrders, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_create(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_detail(request, po_id):
    try:
        purchaseOrder = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchaseOrder)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchaseOrder, data=request.data)
        if serializer.is_valid():
            serializer.save()

            vendor = purchaseOrder.vendor
            vendor.update_average_response_time()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchaseOrder.delete()

        vendor = purchaseOrder.vendor
        vendor.update_average_response_time()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    purchase_order.acknowledgment_date = datetime.now()
    purchase_order.save()

    vendor = purchase_order.vendor
    vendor.update_average_response_time()
    vendor.update_performance_metrics()

    return Response({'message': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)
