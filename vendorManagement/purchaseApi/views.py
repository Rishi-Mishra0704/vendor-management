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
    """
    Checks if the user is authenticated and returns a list of Purchase Orders(PO).

    Fetches all POs from the database and converts them to JSON.
    Returns a JSON response with a list of all POs.
    """
    purchaseOrders = PurchaseOrder.objects.all()
    serializers = PurchaseOrderSerializer(purchaseOrders, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_create(request):
    """
    Checks if the user is authenticated and creates a new PO.

    Takes a JSON payload and creates a new PO instance.
    Returns the serialized PO data in the response on successful creation.
    """
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
    """
    Checks if the user is authenticated and performs CRUD operations on a PO.
    Retrieve, update, or delete a PO.

    - GET: Retrieve details of a specific PO.
    - PUT: Update the details of a specific PO.
    - DELETE: Delete a specific PO.

    Returns the serialized PO data in the response for GET and PUT requests.
    Returns a 204 NO CONTENT response on successful DELETE.
    Returns a 404 NOT FOUND response if the PO does not exist.
    """
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
    """
    Checks if the user is authenticated and acknowledge a purchase order and update vendor performance metrics.

    - POST:
        - Acknowledge a purchase order by updating its acknowledgment date.
        - Update the average response time for the vendor.
        - Update all performance metrics for the vendor.
        - Return a success message in the response.

    Parameters:
    - po_id: The ID of the purchase order to be acknowledged.

    Returns:
    - Response: A JSON response indicating the success of the acknowledgment.
    """
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    purchase_order.acknowledgment_date = datetime.now()
    purchase_order.save()

    vendor = purchase_order.vendor
    vendor.update_average_response_time()
    vendor.update_performance_metrics()

    return Response({'message': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)
