from django.shortcuts import get_object_or_404
from django.db.models import Avg, F
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import HistoricalPerformance
from vendorApi.models import Vendor

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Update the performance metrics before retrieving historical performance
    vendor.update_performance_metrics()
    vendor.save()
    performances = HistoricalPerformance.objects.filter(vendor=vendor)
    print(f"Vendor Metrics After Update: {vendor.on_time_delivery_rate}, {vendor.quality_rating_avg}, {vendor.average_response_time}, {vendor.fulfillment_rate}")

    if performances.count() > 0:
        on_time_delivery_rate = performances.aggregate(Avg('on_time_delivery_rate'))[
            'on_time_delivery_rate__avg']
        quality_rating_avg = performances.aggregate(Avg('quality_rating_avg'))[
            'quality_rating_avg__avg']
        average_response_time = performances.aggregate(Avg('average_response_time'))[
            'average_response_time__avg']
        fulfillment_rate = performances.aggregate(Avg('fulfillment_rate'))[
            'fulfillment_rate__avg']
    else:
        on_time_delivery_rate = quality_rating_avg = average_response_time = fulfillment_rate = None

    
    print(f"Historical Performance Metrics: {on_time_delivery_rate}, {quality_rating_avg}, {average_response_time}, {fulfillment_rate}")
    return Response({
        'vendor': vendor.id,
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    })