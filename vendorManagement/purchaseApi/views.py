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
    

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Acknowledge Purchase Order

    # Update Average Response Time
    vendor = purchase_order.vendor
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_response_time = sum([(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos])
    vendor.average_response_time = total_response_time / acknowledged_pos.count() if acknowledged_pos.count() > 0 else 0
    vendor.save()

    # Update Fulfillment Rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    successful_fulfillment_pos = completed_pos.exclude(quality_rating=None)  # Modify condition based on your definition of successful fulfillment
    
    vendor.fulfillment_rate = (successful_fulfillment_pos.count() / completed_pos.count()) * 100
    vendor.save()

    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)