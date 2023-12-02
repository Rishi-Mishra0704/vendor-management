from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import HistoricalPerformance
from vendorApi.models import Vendor

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Update the performance metrics before creating historical performance
    vendor.update_performance_metrics()

    # Create a new historical performance record using the vendor's metrics
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate,
    )

    # Directly use the metrics from the vendor instance in the response
    return Response({
        'vendor': vendor.id,
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate,
    })
