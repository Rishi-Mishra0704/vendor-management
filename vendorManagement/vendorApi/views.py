from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


from .models import Vendor
from .serializer import VendorSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors(request):
    """
    Checks if the user is authenticated and returns a list of vendors.

    Fetches all vendors from the database and converts them to JSON.
    Returns a JSON response with a list of all vendors.
    """
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_create(request):
    """
    Checks if the user is authenticated and creates a new vendor.

    Takes a JSON payload and creates a new vendor instance.
    Returns the serialized vendor data in the response on successful creation.
    """

    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_detail(request, vendor_id):
    """
    Checks if the user is authenticated and performs CRUD operations on a vendor.
    Retrieve, update, or delete a vendor.

    - GET: Retrieve details of a specific vendor.
    - PUT: Update the details of a specific vendor.
    - DELETE: Delete a specific vendor.

    Returns the serialized vendor data in the response for GET and PUT requests.
    Returns a 204 NO CONTENT response on successful DELETE.
    Returns a 404 NOT FOUND response if the vendor does not exist.
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    """
    Checks if the user is authenticated and Retrieve performance metrics for a vendor.

    - GET: Retrieve performance metrics such as on-time delivery rate, quality rating,
    average response time, and fulfillment rate for a specific vendor.

    Returns a JSON response with the performance metrics.
    Returns a 404 NOT FOUND response if the vendor does not exist.
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    vendor.update_performance_metrics()

    data = {
        'vendor': vendor.id,
        "on_time_delivery": vendor.on_time_delivery_rate,
        "quality_rating": vendor.quality_rating_avg,
        "average_response_time": vendor.average_response_time,
        "fulfillment_rate": vendor.fulfillment_rate,
    }

    return Response(data)
